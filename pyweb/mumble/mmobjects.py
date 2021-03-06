# -*- coding: utf-8 -*-
# kate: space-indent on; indent-width 4; replace-tabs on;

"""
 *  Copyright © 2009-2010, Michael "Svedrin" Ziegler <diese-addy@funzt-halt.net>
 *
 *  Mumble-Django is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This package is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
"""

import base64
import socket
import datetime
import re
from time import time

from django.contrib.sites.models import Site
from django.utils.http import urlquote
from django.conf import settings

from mumble.utils import iptostring

def cmp_channels( left, rite ):
    """ Compare two channels, first by position, and if that equals, by name. """
    if hasattr( left, "position" ) and hasattr( rite, "position" ):
        byorder = cmp( left.position, rite.position )
        if byorder != 0:
            return byorder
    return cmp_names( left, rite )

def cmp_names( left, rite ):
    """ Compare two objects by their name property. """
    return cmp( left.name, rite.name )

def xmlpopulate( node, srcobj ):
    """ Read all instance variables from srcobj and set them as attributes on the given node. """
    for key in srcobj.__dict__:
        val = getattr( srcobj, key )
        if   isinstance( val, bool ):
            encoded = unicode(val).lower()
        elif isinstance( val, list ) or isinstance( val, tuple ):
            encoded = ' '.join( ( unicode(elem) for elem in val ) )
        elif isinstance( val, str ):
            encoded = unicode(val, "utf8")
        else:
            encoded = unicode(val)
        if "\x00" in encoded: # user::context. no kidding. complain to pcgod plzkthx.
            node.set( key, base64.encodestring( encoded ) )
        else:
            node.set( key, encoded )

class mmChannel( object ):
    """ Represents a channel in Murmur. """

    def __init__( self, server, channel_obj, parent_chan = None ):
        self.server   = server
        self.players  = list()
        self.subchans = list()
        self.linked   = list()

        self.channel_obj = channel_obj
        self.chanid      = channel_obj.id

        self.parent = parent_chan
        if self.parent is not None:
            self.parent.subchans.append( self )

        self._acl = None

    def __repr__( self ):
        return "mmChannel <%d: %s>" % ( self.chanid, self.name )

    # Lookup unknown attributes in self.channel_obj to automatically include Murmur's fields
    def __getattr__( self, key ):
        if hasattr( self.channel_obj, key ):
            return getattr( self.channel_obj, key )
        else:
            raise AttributeError( "'%s' object has no attribute '%s'" % ( self.__class__.__name__, key ) )

    def parent_channels( self ):
        """ Return the names of this channel's parents in the channel tree. """
        if self.parent is None or self.parent.is_server or self.parent.chanid == 0:
            return []
        return self.parent.parent_channels() + [self.parent.name]


    def getACL( self ):
        """ Retrieve the ACL for this channel. """
        if not self._acl:
            self._acl = mmACL( self, self.server.ctl.getACL( self.server.srvid, self.chanid ) )

        return self._acl

    acl = property( getACL )


    is_server  = False
    is_channel = True
    is_player  = False


    playerCount = property(
        lambda self: len( self.players ) + sum( [ chan.playerCount for chan in self.subchans ] ),
        doc="The number of players in this channel."
        )

    id   = property(
        lambda self: "channel_%d"%self.chanid,
        doc="A string ready to be used in an id property of an HTML tag."
        )

    top_or_not_empty = property(
        lambda self: self.parent is None or self.parent.chanid == 0 or self.playerCount > 0,
        doc="True if this channel needs to be shown because it is root, a child of root, or has players."
        )

    show =  property( lambda self: settings.SHOW_EMPTY_SUBCHANS or self.top_or_not_empty )

    def __str__( self ):
        return '<Channel "%s" (%d)>' % ( self.name, self.chanid )

    def sort( self ):
        """ Sort my subchannels and players, and then iterate over them and sort them recursively. """
        self.subchans.sort( cmp_channels )
        self.players.sort( cmp_names )
        for subc in self.subchans:
            subc.sort()

    def visit( self, callback, lvl = 0 ):
        """ Call callback on myself, then visit my subchans, then my players. """
        callback( self, lvl )
        for subc in self.subchans:
            subc.visit( callback, lvl + 1 )
        for plr in self.players:
            plr.visit( callback, lvl + 1 )


    def getURL( self, for_user = None ):
        """ Create an URL to connect to this channel. The URL is of the form
            mumble://username@host:port/parentchans/self.name
        """
        from urlparse import urlunsplit
        versionstr = "version=%s" % self.server.prettyversion

        if self.parent is not None:
            chanlist = self.parent_channels() + [self.name]
            chanlist = [ urlquote( chan ) for chan in chanlist ]
            urlpath  = "/".join( chanlist )
        else:
            urlpath  = ""

        if for_user is not None:
            netloc = "%s@%s" % ( for_user.name, self.server.netloc )
            return urlunsplit(( "mumble", netloc, urlpath, versionstr, "" ))
        else:
            return urlunsplit(( "mumble", self.server.netloc, urlpath, versionstr, "" ))

    connecturl = property( getURL )

    def setDefault( self ):
        """ Make this the server's default channel. """
        self.server.defchan = self.chanid
        self.server.save()

    is_default = property(
        lambda self: self.server.defchan == self.chanid,
        doc="True if this channel is the server's default channel."
        )

    def asDict( self, authed=False ):
        chandata = self.channel_obj.__dict__.copy()
        chandata['users']        = [ pl.asDict( authed ) for pl in self.players  ]
        chandata['channels']     = [ sc.asDict( authed ) for sc in self.subchans ]
        chandata['x_connecturl'] = self.connecturl
        return chandata

    def asXml( self, parentnode, authed=False ):
        from xml.etree.cElementTree import SubElement
        me = SubElement( parentnode, "channel" )
        xmlpopulate( me, self.channel_obj )

        me.set( "x_connecturl", self.connecturl )

        for sc in self.subchans:
            sc.asXml(me, authed)
        for pl in self.players:
            pl.asXml(me, authed)

    def asMvXml( self, parentnode ):
        """ Return an XML tree for this channel suitable for MumbleViewer-ng. """
        from xml.etree.cElementTree import SubElement
        me      = SubElement( parentnode, "item" , id=self.id, rel='channel' )
        content = SubElement( me,         "content" )
        name    = SubElement( content ,   "name" )
        name.text = self.name

        for sc in self.subchans:
            sc.asMvXml(me)
        for pl in self.players:
            pl.asMvXml(me)

    def asMvJson( self ):
        """ Return a Dict for this channel suitable for MumbleViewer-ng. """
        return  {
            "attributes": {
                "href": self.connecturl,
                "id":   self.id,
                "rel":  "channel",
                },
            "data": self.name,
            "children": [ sc.asMvJson() for sc in self.subchans ] + \
                    [ pl.asMvJson() for pl in self.players  ],
            "state": { False: "closed", True: "open" }[self.top_or_not_empty],
            }



class mmPlayer( object ):
    """ Represents a Player in Murmur. """

    def __init__( self, server, player_obj, player_chan ):
        self.player_obj    = player_obj

        self.onlinesince  = datetime.datetime.fromtimestamp( float( time() - player_obj.onlinesecs ) )
        self.channel      = player_chan
        self.channel.players.append( self )

        if self.isAuthed:
            from mumble.models import MumbleUser
            try:
                self.mumbleuser = MumbleUser.objects.get( mumbleid=self.userid, server=server )
            except MumbleUser.DoesNotExist:
                self.mumbleuser = None
        else:
            self.mumbleuser = None

    def __repr__( self ):
        return "mmPlayer <%d: %s (%d)>" % ( self.session, self.name, self.userid )

    # Lookup unknown attributes in self.player_obj to automatically include Murmur's fields
    def __getattr__( self, key ):
        if hasattr( self.player_obj, key ):
            return getattr( self.player_obj, key )
        else:
            raise AttributeError( "'%s' object has no attribute '%s'" % ( self.__class__.__name__, key ) )

    def __str__( self ):
        return '<Player "%s" (%d, %d)>' % ( self.name, self.session, self.userid )

    hasComment = property(
        lambda self: hasattr( self.player_obj, "comment" ) and bool(self.player_obj.comment),
        doc="True if this player has a comment set."
        )

    isAuthed = property(
        lambda self: self.userid != -1,
        doc="True if this player is authenticated (+A)."
        )

    isAdmin = property(
        lambda self: self.mumbleuser and self.mumbleuser.getAdmin(),
        doc="True if this player is in the Admin group in the ACL."
        )

    # Totally ripped from Pimmetje
    isTalking = property( lambda self: self.idlesecs == 0, doc="True if this player is currently talking." )

    is_server  = False
    is_channel = False
    is_player  = True

    def getIpAsString( self ):
        """ Get the client's IPv4 or IPv6 address, in a pretty format. """
        return iptostring(self.player_obj.address)

    ipaddress = property( getIpAsString )
    fqdn      = property( lambda self: socket.getfqdn( self.ipaddress ),
        doc="The fully qualified domain name of the user's host." )

    # kept for compatibility to mmChannel (useful for traversal funcs)
    playerCount = property( lambda self: -1, doc="Exists only for compatibility to mmChannel." )

    id = property(
        lambda self: "player_%d"%self.session,
        doc="A string ready to be used in an id property of an HTML tag."
        )

    def visit( self, callback, lvl = 0 ):
        """ Call callback on myself. """
        callback( self, lvl )

    def asDict( self, authed=False ):
        pldata = self.player_obj.__dict__.copy()

        if "address" in pldata:
            if authed:
                pldata["x_addrstring"] = self.ipaddress
            else:
                del pldata["address"]

        if self.channel.server.hasUserTexture(self.userid):
            from views import showTexture
            from django.core.urlresolvers import reverse
            textureurl = reverse( showTexture, kwargs={ 'server': self.channel.server.id, 'userid': self.userid } )
            pldata['x_texture'] = "http://" + Site.objects.get_current().domain + textureurl

        if self.mumbleuser and self.mumbleuser.gravatar:
            pldata['x_gravatar'] = self.mumbleuser.gravatar

        return pldata

    def asXml( self, parentnode, authed=False ):
        from xml.etree.cElementTree import SubElement
        me = SubElement( parentnode, "user" )
        xmlpopulate( me, self.player_obj )

        if authed:
            me.set( "x_addrstring", self.ipaddress )
        else:
            me.set( "address", "" )

        if self.channel.server.hasUserTexture(self.userid):
            from views import showTexture
            from django.core.urlresolvers import reverse
            textureurl = reverse( showTexture, kwargs={ 'server': self.channel.server.id, 'userid': self.userid } )
            me.set( 'x_texture', "http://" + Site.objects.get_current().domain + textureurl )

        if self.mumbleuser and self.mumbleuser.gravatar:
            me.set( 'x_gravatar', self.mumbleuser.gravatar )

    def asMvXml( self, parentnode ):
        """ Return an XML node for this player suitable for MumbleViewer-ng. """
        from xml.etree.cElementTree import SubElement
        me      = SubElement( parentnode, "item" , id=self.id, rel='user' )
        content = SubElement( me,         "content" )
        name    = SubElement( content ,   "name" )
        name.text = self.name

    def asMvJson( self ):
        """ Return a Dict for this player suitable for MumbleViewer-ng. """
        return {
            "attributes": {
                "id":   self.id,
                "rel":  "user",
                },
            'data': self.name,
            }



class mmACL( object ):
    """ Represents an ACL for a certain channel. """

    def __init__( self, channel, acl_obj ):
        self.channel = channel
        self.acls, self.groups, self.inherit = acl_obj

        self.groups_dict = {}

        for group in self.groups:
            self.groups_dict[ group.name ] = group

    def group_has_member( self, name, userid ):
        """ Checks if the given userid is a member of the given group in this channel. """
        if name not in self.groups_dict:
            raise ReferenceError( "No such group '%s'" % name )

        return userid in self.groups_dict[name].add or userid in self.groups_dict[name].members

    def group_add_member( self, name, userid ):
        """ Make sure this userid is a member of the group in this channel (and subs). """
        if name not in self.groups_dict:
            raise ReferenceError( "No such group '%s'" % name )

        group = self.groups_dict[name]

        # if neither inherited nor to be added, add
        if userid not in group.members and userid not in group.add:
            group.add.append( userid )

        # if to be removed, unremove
        if userid in group.remove:
            group.remove.remove( userid )

    def group_remove_member( self, name, userid ):
        """ Make sure this userid is NOT a member of the group in this channel (and subs). """
        if name not in self.groups_dict:
            raise ReferenceError( "No such group '%s'" % name )

        group = self.groups_dict[name]

        # if added here, unadd
        if userid in group.add:
            group.add.remove( userid )
        # if member and not in remove, add to remove
        elif userid in group.members and userid not in group.remove:
            group.remove.append( userid )

    def save( self ):
        """ Send this ACL to Murmur. """
        return self.channel.server.ctl.setACL(
            self.channel.server.srvid,
            self.channel.chanid,
            self.acls, self.groups, self.inherit
            )



