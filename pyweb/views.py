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

from django.shortcuts            import render_to_response
from django.template            import RequestContext
from django.contrib.auth.decorators    import login_required

from mumble.models            import MumbleUser

@login_required
def profile( request ):
    userdata = {
        "ProfileActive": True,
        "mumbleaccs":    MumbleUser.objects.filter(    owner  = request.user ),
        }

    return render_to_response(
        'registration/profile.html',
        userdata,
        context_instance = RequestContext(request)
        )


def imprint( request ):
    import mumble
    return render_to_response(
        'registration/imprint.html',
        { 'upstreamversion': mumble.getLatestUpstreamVersion() },
        context_instance = RequestContext(request) )
