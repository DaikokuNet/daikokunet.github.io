#!/usr/bin/perl

# ↑ プロバイダの指定に従ってPerlのパスを変更してください
# - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - -
# ↓ このCGIはjcode.pmもしくはjcode.plが必要です。jcode.pmを用いる場合は1、
#	  そうでない場合は0を指定してください。

$use_jcode_pm = 1;


# - - - - - - - - - - - - - - - - - - - -
# ↓ ログを見るために必要なバスワードを指定します。

$pswd = '4126';


# - - - - - - - - - - - - - - - - - - - -
# ↓ データを保存するファイル名を指定します。

$file_name = 'accesslog.txt';



# - - - - - - - - - - - - - - - - - - - -
# ↓ 残しておくログの数です。
#	 1000個でデータファイルサイズが200KBぐらいが目安です。
#	 5000個が最大値です。100～5000の範囲で指定してください。

$log_count = 5000;


# - - - - - - - - - - - - - - - - - - - -
# ↓ サーバー時間と日本時間の差。日本時間より3時間遅れていれば3とします
#

$timedif = 0;


# - - - - - - - - - - - - - - - - - - - -
# ↓ 自分(管理者)のログを残すか(1)残さなか(0)を指定します

$selflog = 0;

# - - - - - - - - - - - - - - - - - - - -
# ↓ 以下の文字を含むリンク元を表示しないようにします。


@own = (
		'http://www.daikokunet.jp/'
	);


# - - - - - - - - - - - - - - - - - - - -
# ↓ ブラウザの対応表です。ブラウザが送信してくる文字列に
#	 左側の文字列が含まれた場合、右側の表示名を使います。
#	 通常設定の必要はありません。

@browser = (
			'MSIE 7.0', 					'Internet Explorer 7.0',
			'MSIE 6.0', 					'Internet Explorer 6.0',
			'MSIE 5.5', 					'Internet Explorer 5.5',
			'MSIE 5.2',						'Internet Explorer 5.2',
			'MSIE 5.1',						'Internet Explorer 5.1',
			'MSIE 5.0', 					'Internet Explorer 5.0',
			'MSIE 4.0',						'Internet Explorer 4.0',
			'MSIE 3.0',						'Internet Explorer 3.0',

			'Netscape/7.0', 				'Netscape 7.0',
			'Netscape6/6.2',				'Netscape 6.2',
			'Netscape6/6.1',				'Netscape 6.1',
			'Mozilla/4.7',					'Netscape 4.7',
			'Mozilla/4.6',					'Netscape 4.6',
			'Mozilla/4.5',					'Netscape 4.5',
			'Mozilla/4.09',					'Netscape 4.0',
			'Mozilla/4.08',					'Netscape 4.0',
			'Mozilla/4.07',					'Netscape 4.0',
			'Mozilla/4.06',					'Netscape 4.0',
			'Mozilla/4.05',					'Netscape 4.0',
			'Mozilla/4.04',					'Netscape 4.0',
			'Mozilla/4.03',					'Netscape 4.0',
			'Mozilla/4.02',					'Netscape 4.0',
			'Mozilla/4.01',					'Netscape 4.0',
			'Mozilla/4.0 [',				'Netscape 4.0',

			'Opera/6.0',					'Opera 6.0',
			'Opera 6.0',					'Opera 6.0',
			'Opera/5.0',					'Opera 5.0',

			'rv:1.2',						'Mozilla 1.2',
			'rv:1.1',						'Mozilla 1.1',
			'rv:1.0',						'Mozilla 1.0',
			'rv:0.9',						'Mozilla 0.9',

			'Sleipnir',						'Sleipnir',
			'Galeon',						'Galeon',
			'DreamPassport',				'DreamPassport',
			'Lynx',							'Lynx',
			'Ｎ209',						'i-mode',

			'Mozilla/3.01 (compatible;)',	'unknown',
			'unknown','unknown'
		);


# - - - - - - - - - - - - - - - - - - - -
# ↓ OSの対応表です。ブラウザが送信してくる文字列に
#	 左側の文字列が含まれた場合、右側の表示名を使います。
#	 通常設定の必要はありません。

@os = (
			'Windows NT 5.1', 			'Windows XP',
			'Windows XP',				'Windows XP',
			'Windows NT 5.0', 			'Windows 2000',
			'Windows 2000', 			'Windows 2000',
			'Windows NT 4.0', 			'Windows NT',
			'Windows NT'	, 			'Windows NT',
			'WinNT',					'Windows NT',
			'Windows ME',				'Windows ME',
			'Windows 98; Win 9x 4.90', 	'Windows ME',
			'Windows 98', 				'Windows 98',
			'Win98',					'Windows 98',
			'Windows 95', 				'Windows 95',
			'Win95',					'Windows 95',

			'FreeBSD',					'FreeBSD',

			'Macintosh',				'Macintosh',
			'Mac_PowerPC',				'Macintosh',

			'DreamPassport',			'DreamCast',

			'Debian',					'Linax',
			'Linux',					'Linax',


			'unknown','unknown'
		);

# - - - - - - - - - - - - - - - - - - - -
#  これ以降は編集しないでください。
# - - - - - - - - - - - - - - - - - - - -
$cnt_par_page = 300;
$version = '1.50';

eval "use Jcode;";
if($@) {
	require 'jcode.pl';
	$use_jcode_pm = 0;
}


if($log_count > 5000){
	$log_count = 5000;
}
if($log_count < 100){
	$log_count = 100;
}
$cookie = '';
$cookies{'pswd'} = '';
#$cgi_name = 'http://' . $ENV{'SERVER_NAME'} . ($ENV{'REQUEST_URI'} || $ENV{'DOCUMENT_URI'} || $ENV{'SCRIPT_NAME'});

$cgi_name = 'http://cgi.geocities.jp/daikoku_yu/accesslog.cgi';

$soft_garakuta = 'http://www.bc.wakwak.com/~wmasayoshi/soft/';

($cgi_name) = split(/\?/,$cgi_name);

unless(-e $file_name){
	open(F,">$file_name");
	close(F);
}

&init_form('sjis');
&init_cookie();
local($date) = &gmt_string(7 * 24 * 60 * 60);
$form{'pswd'} && ($cookies{'pswd'} = $form{'pswd'});
$cookie = "Set-Cookie: pswd=$cookies{'pswd'}; expires=$date; ";

local(%title) = ('day','日付別アクセス数','time','時間帯別アクセス数','url','ページ別アクセス数','ref','リンク元','browser','ブラウザ別アクセス数','os','OS別アクセス数','qt','検索文字列');

if($form{'add'}){
	if($selflog || $cookies{'pswd'} ne $pswd){
		&add_log();
	}
	print "Content-Type: image/gif\n";
	print "Content-Length: 42\n\n";
	local($data) = '47494638396101000100800000ffffff00000021f90401000000002c0000000001000100000202440100';
	local($i);
	for($i=0;$i<length($data);$i+=2){
	   print pack("C", hex(substr($data,$i,2)));
	}
}elsif($form{'pswd'} ne $pswd && $cookies{'pswd'} ne $pswd){
	if($form{'pswd'} ne ''){
		&print_login('wrong');
	}else{
		&print_login();
	}
}elsif($form{'view'} eq 'browser'){
	&print_begin();
	&print_graph($title{'browser'});
	$form{'view'} = 'os';
	&print_graph($title{'os'});
	&print_end();
}elsif($form{'view'} eq 'tag'){
	&print_begin();
	&print_tag();
	&print_end();
}elsif($form{'view'} eq 'info'){
	&print_begin();
	&print_info();
	&print_end();
}elsif($title{$form{'view'}}){
	&print_begin();
	&print_graph($title{$form{'view'}});
	&print_end();
}else{
	&print_begin();
	&print_log();
	&print_end();
}
exit(0);
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub print_info
{
print<<"EOF";
<font size="+2"><b><i>サーバー情報</i></b></font>
<hr width="100%">
EOF
local(@info);
if($use_jcode_pm){
	push(@info,'Jcode.pm','利用可');
}else{
	push(@info,'jcode.pm','利用不可','Jcode.pl','利用可');
}
open(F,"<$file_name");
eval('flock(F,2);');
push(@info,'Perlのバージョン',"Version $]");
push(@info,'サーバーソフト',$ENV{'SERVER_SOFTWARE'});
push(@info,"ファイルロック");
if($@){
	push(@info,"使用不可($@)");
}else{
	push(@info,"使用可");
}
close(F);
local($i) = 0;
print '<table>';
for($i=0;$i<=$#info;$i+=2){
	print "<tr><td><b>$info[$i]</b></td><td>：</td><td>$info[$i+1]</td></tr>";
}
print '</table>';
print '<hr width="100%">';
print '<font size="+2"><b><i>設定情報</i></b></font>';
print '<hr width="100%">';
@info = ();
local $size = -s $file_name;
$size = int(($size + 1023) / 1024) . " KB";
push(@info,"AccessLog CGIのバージョン","Version $version");
push(@info,"データファイル","$file_name ($size)");
push(@info,"残しておくログの数","$log_count 件");
push(@info,"サーバーとの時差","$timedif 時間");
push(@info,"管理者自身のログ",$selflog ? '残す' : '残さない');
print '<table>';
for($i=0;$i<=$#info;$i+=2){
	print "<tr><td><b>$info[$i]</b></td><td>：</td><td>$info[$i+1]</td></tr>";
}
print '</table>';
print '<hr width="100%">';
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub print_graph
{
	local($title) = @_;

print<<"EOF";
<font size="+2"><b><i>$title</i></b></font>　<a href="$cgi_name?view=$form{'view'}&sort=value">アクセス数順</a>　<a href="$cgi_name?view=$form{'view'}&sort=key">名前順</a>
<hr width="100%">
EOF
	local($i,*F,%item,$max);
	local(%offset) = ('day',0,'time',0,'url',1,'ref',2,'browser',4,'os',4,'qt',2);

	open(F,"<$file_name");
	eval('flock(F,2);');
	seek(F,0,0);
	for(1 .. $offset{$form{'view'}}){
		<F>;
	}
	while(<F>){
		local($item) = &get_item($_);
		if($item ne ''){
			$item{$item}++;
			$max = $max < $item{$item} ? $item{$item} : $max;
		}
		for(1 .. 4){
			<F>
		}
	}

	close(F);
	local(%unit) = ('time','時');
	foreach (&sort_item($form{'sort'},%item)){
		local($key) = $_;
		print "$key$unit{$form{'view'}} : $item{$key}件<br>";
		print '<div align="left"><hr " width="' . int(95*$item{$key}/$max) . '%" size=12 color="blue"></div>';
	}
	print "<hr width=\"100%\">\n";
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub get_item
{
	local($item) = @_;
	chop($item);
	local($type) = $form{'view'};
	if($type eq 'day'){
		($item) = split(/\s/,$item);
	}elsif($type eq 'time'){
		local(@item) = split(/[\/:\s]/,$item);
		$item[3] || ($item[3] = $item[4]);
		$item = $item[3] < 10 ? "0$item[3]" : $item[3];
	}elsif($type eq 'url'){
		($item) = split(/\?/,$item);
	}elsif($type eq 'ref'){
		if($item eq ''){
			$item = 'bookmark';
		}else{
			($item) = split(/\?/,$item);
			foreach(@own){
				if(index($item,$_) == 0){
					$item = '';
				}
			}
			end:
		}
	}elsif($type eq 'browser'){
		$item = &get_browser_name($item);
	}elsif($type eq 'os'){
		$item = &get_os_name($item);
	}elsif($type eq 'qt'){
		local(@itm);
		local(@qt) = split(/[&\?]/,$item);
		$item = '';
		foreach (@qt){
			local($qt) = $_;
			local(@ck) = ('query=','qt=','search=','MT=','q=','kw=','q=');
			foreach (@ck){
				local($str) = $_;
				if(0==index($qt,$str)){
					$item = substr($qt,length($str));
					$item =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
					if($use_jcode_pm){
						&Jcode::convert(\$item, 'sjis', &Jcode::getcode( $item ) );
					}else{
						&jcode'convert(*item, 'sjis');
					}
				}
			}
		}
	}
	return $item;
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub sort_item
{
	local($type,%item) = @_;

	local(@keys);

	if($type eq 'key'){
		@keys = sort keys %item;
	}else{
		@keys = sort {$item{$b} <=> $item{$a}} keys %item;
	}
	return @keys;
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub print_tag
{
local($url) = $cgi_name;
print<<"EOF";
アクセスログを取るHTMLに以下のタグを入力してください。&lt;/body&gt;の直前を推奨します。<br>
<form onsubmit="return false;">
<textarea cols=80 rows=6>
<script language="JavaScript">
<!--
document.write('<img width=1 height=1 '
	+ 'src="$url?ref='
	+ escape(document.referrer)
	+ '&add=1">');
// -->
</script>
</textarea>
<hr width="100%">
EOF
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub print_begin
{
print<<"EOF";
Content-Type: text/html
$cookie

<html>
<head>
  <title>アクセスログの解析 Version $version</title>
  <meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
</head>
<body>
<font size="-1">
<a href="$cgi_name?view=log">ログ</a> －
<a href="$cgi_name?view=qt">検索文字列別</a> －
<a href="$cgi_name?view=day&sort=key">日付別</a> －
<a href="$cgi_name?view=time&sort=key">時間別</a> －
<a href="$cgi_name?view=url&sort=value">ページ別</a> －
<a href="$cgi_name?view=ref&sort=value">リンク元別</a> －
<a href="$cgi_name?view=browser&sort=value">ブラウザ別</a> －
<a href="$cgi_name?view=tag">挿入タグの取得</a> －
<a href="$cgi_name?view=info">サーバー・設定情報</a>
</font>
<hr width="100%">
EOF
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub print_end
{
print<<"EOF";
<font size="-1">
<a href="$cgi_name?view=log">ログ</a> －
<a href="$cgi_name?view=qt">検索文字列別</a> －
<a href="$cgi_name?view=day&sort=key">日付別</a> －
<a href="$cgi_name?view=time&sort=key">時間別</a> －
<a href="$cgi_name?view=url&sort=value">ページ別</a> －
<a href="$cgi_name?view=ref&sort=value">リンク元別</a> －
<a href="$cgi_name?view=browser&sort=value">ブラウザ別</a> －
<a href="$cgi_name?view=tag">挿入タグの取得</a> －
<a href="$cgi_name?view=info">サーバー・設定情報</a>
</font>
<hr width="100%">
EOF
print '<div align="right"><font size="-1">このCGIは<a href="' . $soft_garakuta . '">ソフトのがらくた箱</a>にて配布しています。</font></div>';
print "\n</body>\n</html>\n";
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub print_log
{
print<<"EOF";
<font size="+2"><b><i>アクセスログ</i></b></font>　<a href="$cgi_name?view=log&sort=new">新しい順</a>　<a href="$cgi_name?view=log&sort=old">古い順</a>
<hr width="100%">
EOF
	local($i,*F);
	open(F,"<$file_name");
	eval('flock(F,2);');
	seek(F,0,0);

	local($curr_page) = -1;
	local(@data) = <F>;
	do{
		$curr_page++;
		local($b,$e) = '';
		local($end) = $cnt_par_page * $curr_page + $cnt_par_page < ($#data + 1) / 5 ? $cnt_par_page * $curr_page + $cnt_par_page : ($#data + 1) / 5;
		if($curr_page == int($form{'page'})){
			$b = '<font size="-1"><b>';
			$e = '</b></font>';
		}else{
			$b = "<font size=\"-1\"><a href=\"$cgi_name?view=log&sort=$form{'sort'}&page=$curr_page\">";
			$e = '</a></font>';
		}
		print "${b}～$end$e";
		print '　';
	}while($cnt_par_page * $curr_page + $cnt_par_page < ($#data + 1) / 5);
	print '<hr width="100%">';
	print "\n";

	if($form{'sort'} eq 'old'){
		local($i);
		for($i=$cnt_par_page * int($form{'page'});$i<$cnt_par_page * (int($form{'page'})+1) && $i<($#data+1)/5;$i++){
			print '<tt>time &nbsp;&nbsp;&nbsp;: </tt>' . $data[5*$i]  . '<br>';
			print '<tt>url &nbsp;&nbsp;&nbsp;&nbsp;: </tt>' . $data[5*$i+1] . '<br>';
			print '<tt>ref &nbsp;&nbsp;&nbsp;&nbsp;: </tt>' . $data[5*$i+2] . '<br>';
			print '<tt>host &nbsp;&nbsp;&nbsp;: </tt>' . $data[5*$i+3] . '<br>';
			print '<tt>browser : </tt>' . $data[5*$i+4] . '<br>';
			print '<hr width="100%">' . "\n";
		}
	}else{
		local($i);
		for($i=$cnt_par_page * int($form{'page'});$i<$cnt_par_page * (int($form{'page'})+1) && $i<($#data+1)/5;$i++){
			print '<table border=0 cellpadding=0 cellspacing=0>';
			print '<tr><td>time   </td><td>：</td><td>' . $data[$#data - (5*$i+4)] . '</td></tr>';
			print '<tr><td>url	  </td><td>：</td><td>' . $data[$#data - (5*$i+3)] . '</td></tr>';
			print '<tr><td>ref	  </td><td>：</td><td>' . $data[$#data - (5*$i+2)] . '</td></tr>';
			print '<tr><td>host   </td><td>：</td><td>' . $data[$#data - (5*$i+1)] . '</td></tr>';
			print '<tr><td>browser</td><td>：</td><td>' . $data[$#data - (5*$i+0)] . '</td></tr>';
			print '</table><hr width="100%">' . "\n";
		}
	}
	close(F);
}
sub print_ref
{
	local($i,*F,%cnt,$max);
	open(F,"<$file_name");
	eval('flock(F,2);');
	seek(F,0,0);
	<F>;
	<F>;
	while(<F>){
		local($url) = split(/\?/,$_);
		local($ok) = 1;
		foreach(@own){
			(index($url,$_) == 0) && ($ok = 0);
			break;
		}
		if($ok){
			$cnt{$url}++;
			$max = $max < $cnt{$url} ? $cnt{$url} : $max;
		}
		for(1 .. 4){
			<F>
		}
	}
	foreach (sort {$cnt{$b} <=> $cnt{$a}} keys(%cnt)){
		local($key) = $_;
		print "$key : $cnt{$key}件<br>";
	}
	close(F);
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub print_login
{
local $msg = "アクセスログ(Version $version)を閲覧するにはパスワードが必要です。";
if($_[0] eq 'wrong'){
	$msg = '<font color="red"><b>パスワードが違います。</b></font>';
}
local($link) = 'ソフトのがらくた箱';
print<<"EOF";
Content-Type: text/html

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
  <title>アクセスログ</title>
</head>
<body>
$msg
<hr widht="100%">
<form action="$cgi_name" method="POST">
パスワード ： <input type="password" name="pswd" value="${cookies{'pswd'}}"> <input type="submit" value="ログイン">
</form>
<hr width="100%">
<div align="right">このCGIは<a href="$soft_garakuta">$link</a>にて配布されています。</div>
</body>
</html>
EOF
}
sub get_browser_name
{
	local($str) = @_;
	local($i);
	foreach $i (keys %browser){
		if(0 <= index($str,$i)){
			return $browser{$i};
		}
	}
	return $str;
}
sub get_os_name
{
	local($str) = @_;

	local($i);
	foreach $i (keys %os){
		if(0 <= index($str,$i)){
			return $os{$i};
		}
	}
	return $str;
}
sub get_browser_name
{
	local $browser = "[？]$_[0]";


	local $i;
	for($i=0;$i<=$#browser;$i+=2){
		if(0 <= index($_[0],$browser[$i+0])){
			$browser = $browser[$i+1];
		}
	}
	return $browser;
}
sub get_os_name
{
	local $os = "[？]$_[0]";

	local $i;
	for($i=0;$i<=$#os;$i+=2){
		if(0 <= index($_[0],$os[$i+0])){
			$os = $os[$i+1];
		}
	}
	return $os;
}
sub add_log
{
	local(*F);

	$time = &time_string();
	$host = gethostbyaddr(pack("C4", split(/\./, $ENV{'REMOTE_ADDR'})), 2);

	if($host eq ''){
		$host = $ENV{'REMOTE_ADDR'};
	}

	open(F,"+<$file_name");
	eval('flock(F,2);');
	seek(F,0,0);
	local(@data) = <F>;

	seek(F,0,0);

	if(($#data + 1) / 5 < $log_count){
		print F @data;
	}else{
		print F @data[5 .. $#data];
	}

	print F &time_string() . "\n";
	print F $ENV{'HTTP_REFERER'} . "\n";
	print F $form{'ref'} . "\n";
	print F $host . "\n";
	print F $ENV{'HTTP_USER_AGENT'} . "\n";

	truncate(F,tell(F));

	close(F);

}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub gmt_string
{
	local($param) = int($_[0]);
	local(@wday) = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	local(@month) = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	local(@Time) = gmtime(time + $param);
	$Time[5] += 1900;

	for($i=0;$i<=2;$i++){
		if($Time[$i] < 10 ){
			if($i != 2){
				$Time[$i] = "0$Time[$i]";
			}else{
				$Time[$i] = " $Time[$i]";
			}
		}
	}
	return "$wday[$Time[6]], $Time[3]-$month[$Time[4]]-$Time[5] $Time[2]:$Time[1]:$Time[0]";
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub time_string
{
	local(@Time) = localtime(time + $timedif * 60 * 60);
	$Time[5] += 1900;
	$Time[4]++;
	for($i=0;$i<=5;$i++){
		if($Time[$i] < 10){
			if($i != 2){
				$Time[$i] = "0$Time[$i]";
			}else{
				$Time[$i] = " $Time[$i]";
			}
		}
	}
	return "$Time[5]/$Time[4]/$Time[3] $Time[2]:$Time[1]:$Time[0]";
}
#  -  -  -	-  -  -  -	-  -  -  -	-  -
sub init_form {
	local($i,@query, @assocarray, $assoc, $property, $value, $charcode, $method);
	$charcode = $_[0];
	$method = $ENV{'REQUEST_METHOD'};
	$method =~ tr/A-Z/a-z/;
	$query[0] = $ENV{'QUERY_STRING'};
	read(STDIN, $query[1], $ENV{'CONTENT_LENGTH'});
	for($i=0;$i<2;$i++){
		@assocarray = split(/&/, $query[$i]);
		foreach $assoc (@assocarray) {
			($property, $value) = split(/=/, $assoc);
			$value =~ tr/+/ /;
			$value =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
			if($use_jcode_pm){
				&Jcode::convert(\$value, $charcode);
			}else{
				&jcode'convert(*value, $charcode);
			}
			$form{$property} = $value;
		}
	}
}
sub init_cookie
{
	local(@cookies,$i) = split(/; /,$ENV{'HTTP_COOKIE'});
	foreach(@cookies){
		local($key,$value) = split(/=/,$_);
		$cookies{$key} = $value;
	}
}
