��    P      �  k         �  �   �  �   v      �   	     �	     �	     �	     �	     �	  ,   �	     
     9
     I
  *   U
     �
  
   �
     �
     �
     �
     �
     �
  "   �
          #  y   3  ^   �  	     t        �  1   �     �  
   �     �  9   �     1     Q     m     p     }  :   �     �     �  R   �  2   1     d     k     |     �     �     �  	   �     �     �     �     �     �               %     9     H     U  7   h  &   �  >   �  V        ]     b     o     |     �     �     �     �     �     �  !   �  )   �     "    )  �   E  �   �    �  �   �     $     4     B     _     z  (   �      �     �     �  %   �       	        $     +  "   7     Z     c  6   p  0   �     �  o   �  ]   W     �  �   �     Z  ;   w     �     �     �  G   �  $   5     Z     x     {     �  K   �     �  %   �  E     A   _     �     �     �     �  
   �     �  
   �               (     8     =     T     e     v     �     �  "   �  :   �  '     A   4  X   v     �     �     �     �          !     3     I     ^     s      v     �     �        ?   '          0   P      A         M      N      	   1      E                                <              8   #       "      :      /   =          *      C   @   
          D      .       J           %      -   4       +       )                  B   (               !   &         G   ;   2   F                 5      I   $   >   K       3       7      H   9       6   ,      L   O           
          Hint: The texture image <b>needs</b> to be 600x60 in size. If you upload an image with
          a different size, it will be resized accordingly.<br />
         
          You can upload an image that you would like to use as your user texture here.<br />
          Your current texture is:<br />
         
      <b>Hint:</b><br />
      This area is used to display additional information for each channel and player, but requires JavaScript to be
      displayed correctly. You will not see the detail pages, but you can use all links and forms
      that are displayed.
       
      <p>You need to be <a href="%(login_url)s">logged in</a> to be able to register an account on this Mumble server.</p>
     Account owner Admin Admin on root channel Admin:            %(admin)s Administration Another player already registered that name. Authenticated:    %(authed)s Bandwidth [Bps] Boot Server Cannot register player without a password! Channel Channel ID Channel count Channel description Channel name regex Connect DBus or ICE base Deafened by self: %(selfdeafened)s Deafened:         %(deafened)s Default channel Enter the ID of the default channel here. The Channel viewer displays the ID to server admins on the channel detail page. Examples: 'net.sourceforge.mumble.murmur' for DBus or 'Meta:tcp -h 127.0.0.1 -p 6502' for Ice. Full Name Hostname or IP address to bind to. You should use a hostname here, because it will appear on the global server list. IP Obfuscation If on, IP adresses of the clients are not logged. Login password Max. Users Mumble player_id Mumble user %(mu)s on %(srv)s owned by Django user %(du)s Muted by self:    %(selfmuted)s Muted:            %(muted)s No Online since Online users Password required to join. Leave empty for public servers. Player Player name regex Port number %(portno)d is not within the allowed range %(minrange)d - %(maxrange)d Port number to bind to. Use -1 to auto assign one. Public Registered users Registration SSL Certificate SSL Key Server Address Server ID Server Info Server Name Server Password Server Port Server administration Server instance Server instances Server registration Server version Sign-up date Superuser Password The admin group was not found in the ACL's groups list! The password you entered is incorrect. This field must not be updated once the record has been saved. This server is private and protected mode is active. Please enter the server password. User User Texture User account User accounts User name and Login Website Website URL Welcome Message Welcome message Yes You are registered on this server You do not have an account on this server yes,no Project-Id-Version: Mumble-Django v0.8
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2009-07-20 12:43+0200
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: Vid Marić <vid_maric@yahoo.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 
          Savjet: Slika <b>mora</b> biti veličine 600x60. Ako odaberete sliku drugačije veličine, veličina će biti promjenjena u 600x60.<br />
         
          Možete postaviti sliku za koju bi htjeli da zamjeni vašekorisničko ime u Mumble transparentu (overlay).<br />
          Vaša trenutačna slika je:<br />
         
      <b>Savjet:</b><br />
      Ovdje se prikazuju dodatne informacije za svaki kanali svakog igrača te zahtjeva JavaScript kako bi
      se informacije pravilno prikazale. Nećete vidjeti stranicu s detaljima, ali možete koristiti sve linkove i forme.
       
      <p>Morate biti <a href="%(login_url)s">prijavljeni (ulogirani)</a> kako bi ste napravili račun na ovom Mumble serveru.</p>
     Vlasnik računa Administrator Administrator u glavnoj sobi Administrator:   %(admin)s Administracija Ovo ime je zauzeto, probajte neko drugo. Registriran korisnik: %(authed)s Promet [Bps] Pokreni server Odaberite lozinku i probajte ponovno! Soba ID kanala Kanali Opis kanala Dozvoljeni znakovi u nazivu kanala Spoji se DBus ili ICE Samo-utišani zvučnici / slušalice: %(selfdeafened)s Utišani zvučnici / slušalice:    %(deafened)s Početni kanal Unesite ID početnog kanala. Prikaz kanala pokazuje ID administratorima servera na stranici s detaljima kanala. Primjeri: 'net.sourceforge.mumble.murmur' za DBus ili 'Meta:tcp -h 127.0.0.1 -p 6502' za Ice. Ime i prezime Ime poslužitelja (hostname) ili IP adresa adresa za spajanje. Koristite ime poslužitelja ovdje zato što će se pojaviti na globalnoj listi servera. Bilježi IP adrese korisnika Ako je uključeno, IP adrese klijenata se neće bilježiti. Lozinka Maksimalan broj korisnika ID korisnika na Mumbleu Django korisniku %(du)s pripada Mumble račun %(mu)s na serveru %(srv)s Samo-utišan mikrofon: %(selfmuted)s Utišan mikrofon:   %(muted)s Ne Na serveru od Korisnici na serveru Lozinka za pristup serveru. Ostaviti prazno ako se spajate na javni server. Korisnik Dozvoljeni znakovi u nazivu korisnika Port %(portno)d nije u dozvoljenom opsegu %(minrange)d - %(maxrange)d Port za spajanje. Koristite -1 za automatsko dodjeljivanje porta. Javni server Registrirani korisnici Registracija SSL certifikat SSL ključ Adresa servera ID servera Informacije o serveru Ime servera Lozinka servera Port Administracija servera Instanca servera Instance servera Registracija servera Verzija servera Datum registracije Lozinka Superusera (administrator) Grupa administratora nije pronaÄ‘ena u ACL listi grupa! Lozinka koju ste unijeli je neispravna. Ovo polje ne smije biti ažurirano nakon što je zapis spremljen. Ovo je privatan server i potrebna vam je lozinka za pristup. Molimo vas unesite lozinku. Korisnik Korisnička slika Korisnički račun Korisnički računi Korisničko ime Internet stranica URL internet stranice Poruka dobrodošlice Poruka dobrodošlice Da Registrirani ste na ovom serveru Nemate račun na ovom serveru da,ne 