#!/usr/local/bin/perl
# Content-typeヘッダを出力
print "Content-type: text/html\n";

# Set-Cookieヘッダを出力
print "Set-Cookie: ";
print "TEST2=2; ";
print "expires=Friday, 31-Dec-2002 00:00:00 GMT; ";
print "path=/~masa-nak/cgi-bin/cookie; "; 
print "domain=www2s.biglobe.ne.jp\n";

# ヘッダの終わりを出力
print "\n";

print <<EOM;
<HTML>
<HEAD>
<TITLE>TEST</TITLE>
</HEAD>
<BODY>
This is a test.<BR>
$ENV{'HTTP_COOKIE'}
</BODY>
</HTML>
EOM
