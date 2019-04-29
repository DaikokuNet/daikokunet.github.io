#┌─────────────────────────────────
#│ Web Forum v4.8 - 2006/08/03
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'Web Forum v4.8';
#┌─────────────────────────────────
#│[ 注意事項 ]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────
#
# [設置例] かっこ内はパーミッション
#
#    public_html / index.html (ホームページ)
#       |
#       +-- bbs / wforum.cgi   [705]
#            |    wf_regi.cgi  [705]
#            |    wf_admin.cgi [705]
#            |    wf_init.cgi  [604]
#            |    wf_log.cgi   [606]
#            |    jcode.pl     [604]
#            |    fold.pl      [604]
#            |    pastno.dat   [606] ... (過去ログ用)
#            |    title.gif
#            |
#            +-- past [707] / 0001.cgi [606] ... (過去ログ用)
#            |
#            +-- lock [707] /

#---------------------------------------
#  ■基本設定
#---------------------------------------

# 掲示板タイトル名
$title = "Daikoku-NET Web Forum";

# タイトル文字の色
$t_color = "#004080";

# タイトル文字のサイズ
$t_point = '20px';

# タイトル画像を使用するとき
$t_img = "./title.gif";
$t_w = 151; 	# 横サイズ（ピクセル）
$t_h = 28;	# 縦サイズ（ピクセル）

# 本文の文字サイズ
$b_size = '13px';

# 本文の文字フォント
$b_face = 'MS UI Gothic, Osaka, ＭＳ Ｐゴシック';

# パスワード (半角英数字で)
$pass = '41264126';

# 最大記事数
$max = 800;

# 戻り先のＵＲＬ(index.htmlなど)
$home = "http://www.daikokunet.jp/";

# 壁紙・背景色・文字色など
$bg = "";		# 壁紙の指定 (http://から記述)
$bc = "#EEEEEE";	# 背景色
$te = "#004080";	# 文字色
$li = "#0000FF";	# リンク色（未訪問）
$vl = "#008080";	# リンク色（既訪問）
$al = "#DD0000";	# リンク色（訪問中）

# スクリプトURL
$script = './wforum.cgi';

# 管理ファイルURL
$admin = './wf_admin.cgi';

# 書込ファイルURL
$regist = './wf_regi.cgi';

# ログファイル
$logfile = './wf_log.cgi';

# ロックファイル機構
#  0 : 行なわない
#  1 : 行なう（symlink関数式）
#  2 : 行なう（mkdir関数式）
$lockkey = 1;

# ロックファイル名
#  → このディレクトリのパーミッションは777にすること
$lockfile = './lock/wforum.lock';

# URL自動リンク (0=no 1=yes)
$autolink = 1;

# 記事の [題名] の色
$sub_color = "#dd0000";

# 記事下地の色（一括表示時等）
$tbl_color = "#FFFFFF";

# 記事にNEWマークを付ける時間
$new_time = 48;

# NEWマークの表示形態
#  → 画像を使用する場合には $newmark = '<img src="./new.gif">';
#     というように IMGタグを記述してもよい
$newmark = '<font color="#FF3300">new!</font>';

# 記事NOの色
$no_color = "#008000";

# 新着記事一括表示の記事数
$sortcnt = 10;

# 頁あたりツリー表示数
$p_tree = 10;

# リストに表示する「記事タイトル」の最大長（文字数：半角文字換算）
$sub_length = 30;

# メールアドレスの入力を必須 (0=no 1=yes)
$in_email = 0;

# レスがついたらツリー毎トップへ移動 (0=no 1=yes)
$top_sort = 1;

# レスは下から順に付ける (0=no 1=yes)
$bot_res = 1;

# 引用部色変更
#  → ここに色指定を行うと「引用部」を色変更します
#  → この機能を使用しない場合は何も記述しないで下さい ($refcol="";)
$refcol = "#804000";

# 個別画面の上部タイトル色（新着記事など）
$backCol = "#004080";	# 下地色
$charCol = "#ffffff";	# 文字色

# 記事の更新は「method=POST」限定（セキュリティ対策）
#  0 : no
#  1 : yes
$postonly = 1;

# 投稿があるとメール通知する : sendmail必須
#  0 : 通知しない
#  1 : 通知する（自分の記事は送信しない）
#  2 : 通知する（自分の記事も送信する）
$mailing = 2;

# メール通知する際のメールアドレス
$mailto = 'facclog@ybb.ne.jp';

# sendmailパス（メール通知する時）
$sendmail = '/usr/lib/sendmail';

# ツリーのヘッダー記号
$treehead = "▼";

# 過去ログ機能 (0=no 1=yes)
$pastkey = 1;

# 過去ログカウントファイル
$nofile = './pastno.dat';

# 過去ログのディレクトリ（最後は / で閉じる)
$pastdir = './past/';

# 過去ログ１ページ当りの最大行数
#  → これを超えると自動的に次ファイルを生成します
$max_line = 650;

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$gethostbyaddr = 0;

# アクセス制限（半角スペースで区切る、アスタリスク可）
#  → 拒否ホスト名を記述（後方一致）【例】*.anonymizer.com
$deny_host = '*.ap.yournet.ne.jp *.ap.gmo-access.jp *.o-tokyo.nttpc.ne.jp *.d-osaka.nttpc.ne.jp *.p-osaka.nttpc.ne.jp *marunouchi.tokyo.ocn.ne.jp *osakakita.osaka.ocn.ne.jp';
#  → 拒否IPアドレスを記述（前方一致）【例】210.12.345.*
$deny_addr = '49.240.241.168 110.3.96.100 110.3.112.64 126.36.33.113 192.151.156.66 113.230.99.17 122.140.64.200 198.204.226.234 198.204.226.202 123.187.16.8 198.204.226.242  112.252.92.183';

# 禁止ワード
# → 投稿時禁止するワードをコンマで区切る
$no_wd = 'http://,男なら,エロ,見るな,モバゲ,万円,投稿,挿入,デコログ,本番,スター,やってみ,見ちゃ,人妻,入れて,風俗,女性,会員,癒されたい,プレイ,44m4,google,セクロス,財布,バック,shop,online,www.acneonindiajp';

# 日本語チェック（投稿時日本語が含まれていなければ拒否する）
# 0=No  1=Yes
$jp_wd = 1;

# URL個数チェック
# → 投稿コメント中に含まれるURL個数の最大値
$urlnum =0;

# １回当りの最大投稿サイズ (bytes)
$maxData = 51200;

# 他サイトから投稿排除時に指定 (http://から書く)
$baseUrl = '';

# 投稿制限
#  0 : しない
#  1 : 同一IPアドレスからの投稿間隔を制限する
#  2 : 全ての投稿間隔を制限する
$regCtl = 1;

# 制限投稿間隔（秒数）
#  → $regCtl での投稿間隔
$wait = 600;

#---------------------------------------
#  ■設定完了
#---------------------------------------

#---------------------------------------
#  フォームデコード
#---------------------------------------
sub decode {
	$post_flag = 0;
	local($buf);
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag = 1;
		if ($ENV{'CONTENT_LENGTH'} > $maxData) {
			&error("投稿量が大きすぎます");
		}
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$buf = $ENV{'QUERY_STRING'};
	}
	undef(%in);
	foreach ( split(/&/, $buf) ) {
		local($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# S-JIS変換
		&jcode'convert(*val, "sjis", "", "z");

		# タグ処理
		$val =~ s/\t//g;
		$val =~ s/&/&amp;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/\r\n/\t/g;
		$val =~ s/\r/\t/g;
		$val =~ s/\n/\t/g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$mode = $in{'mode'};
	$page = $in{'page'};
	if ($page eq "") { $page = 0; }
	$in{'pastlog'} =~ s/\D//g;

	# 強制改行
	if (($mode eq "form" && $in{'pview'} ne "on" && $in{'wrap'} eq "hard") || ($mode eq "regist" && $in{'wrap'} eq "hard")) {
		local($tmp);
		while ( length($in{'message'}) ) {
			($folded, $in{'message'}) = &fold($in{'message'}, 64);
			$tmp .= "$folded\t";
		}
		$in{'message'} = $tmp;
	}

	# コメント改行コード処理
	while ( $in{'message'} =~ /\t$/ ) { $in{'message'} =~ s/\t$//g; }
	$in{'message'} =~ s/\t/<br>/g;

	# タイムゾーンを日本時間に合わせる
	$ENV{'TZ'} = "JST-9";
	$headflag = 0;
	$lockflag = 0;
}

#---------------------------------------
#  ロック処理
#---------------------------------------
sub lock {
	local($retry) = 5;

	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 30) { &unlock; }
	}
	# symlink関数式ロック
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	# mkdir関数式ロック
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}
	$lockflag = 1;
}

#---------------------------------------
#  ロック解除
#---------------------------------------
sub unlock {
	if ($lockkey == 1) {
		unlink($lockfile);
	} elsif ($lockkey == 2) {
		rmdir($lockfile);
	}

	$lockflag = 0;
}

#---------------------------------------
#  HTMLヘッダ
#---------------------------------------
sub header {
	local($meta) = @_;

	if ($headflag) { return; }
	if ($bg) { $bg = "background=\"$bg\""; }

	print "Content-type: text/html\n\n";
	print <<EOM;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
body,tr,td,th { font-size:$b_size; font-family:"$b_face"; }
a:hover       { text-decoration:underline; color:$al; }
.num          { font-family:Verdana,Helvetica,Arial; }
.obi          { background-color:$backCol; color:$charCol; }
-->
</STYLE>
EOM

	print "$meta\n" if ($meta);

	print <<EOM;
<title>$title</title></head>
<body bgcolor="$bc" text="$te" link="$li" vlink="$vl" alink="$al" $bg>
EOM
	$headflag = 1;
}

#---------------------------------------
#  エラー処理
#---------------------------------------
sub error {
	&unlock if ($lockflag);

	&header();
	print <<EOM;
<div align="center">
<hr width="400">
<h3>ERROR !</h3>
<font color="#dd0000">$_[0]</font>
<p>
<hr width="400">
<p>
<form>
<input type="button" value="前画面にもどる" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#---------------------------------------
#  アクセス制限
#---------------------------------------
sub axsCheck {
	# IP&ホスト取得
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}

	# IPチェック
	local($flg);
	foreach ( split(/\s+/, $deny_addr) ) {
		s/\./\\\./g;
		s/\*/\.\*/g;

		if ($addr =~ /^$_/i) { $flg = 1; last; }
	}
	if ($flg) {
		&error("アクセスを許可されていません");

	# ホストチェック
	} elsif ($host) {

		foreach ( split(/\s+/, $deny_host) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;

			if ($host =~ /$_$/i) { $flg = 1; last; }
		}
		if ($flg) {
			&error("アクセスを許可されていません");
		}
	}
	if ($host eq "") { $host = $addr; }
}

#---------------------------------------
#  時間取得
#---------------------------------------
sub get_time {
	local($time, $log) = @_;
	local($date);

	$time ||= time ;
	local($min,$hour,$day,$mon,$year,$wday) = (localtime($time))[1..6];

	if ($log eq "log") {
		$date = sprintf("%02d/%02d/%02d-%02d:%02d",
				$year-100,$mon+1,$day,$hour,$min);
	} else {
		@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
		$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
				$year+1900,$mon+1,$day,$week[$wday],$hour,$min);
	}
	$date;
}

#---------------------------------------
#  ホスト名取得
#---------------------------------------
sub get_host {
	# IP,ホスト取得
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr;
	}
}

#---------------------------------------
#  入力チェック
#---------------------------------------
sub chk_form {
	local($err);

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	# 他サイトからのアクセスを排除
	if ($baseUrl) {
		$baseUrl =~ s/(\W)/\\$1/g;
		local($ref) = $ENV{'HTTP_REFERER'};
		$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
		if ($ref && $ref !~ /$baseUrl/i) { &error("不正なアクセスです"); }
	}

	# チェック
	if ($no_wd) { &no_wd; }
	if ($jp_wd) { &jp_wd; }
	if ($urlnum > 0) { &urlnum; }

	if ($in{'name'} eq "" || $in{'name'} =~ /^(\x81\x40|\s)+$/)
		{ $err .= "名前の入力モレです<br>"; }
	if ($in{'message'} eq "" || $in{'message'} =~ /^(\x81\x40|\s|<br>)+$/)
		{ $err .= "コメントの入力モレです<br>"; }
	if ($in_email && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/)
		{ $err .= "E-Mailの入力が不正です<br>"; }
	if ($in{'sub'} eq "" || $in{'sub'} =~ /^(\x81\x40|\s)+$/)
		{ $err .= "題名の入力モレです<br>"; }
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }

	if ($err) { &error($err); }
}

#---------------------------------------
#  投稿フォーム部
#---------------------------------------
sub msg_form {
	# クッキー取得
	local($cname,$cmail,$curl,$cpwd,$cpv,$csmail) = &get_cookie;
	$curl ||= 'http://';

	# 修正時
	if ($_[0] eq "edt") {
		($type,$cname,$cmail,$curl,$csmail,$res_sub,$res_msg,$wrap) = @_;

#		$res_msg =~ s/"/&quot;/g;
		if (!$wrap) { $wrap = 'soft'; }
		print "<form><input type=button value='前画面に戻る' onClick='history.back()'></form>\n";
		print "<h3>修正フォーム</h3>\n";
		print "<form action=\"$regist\" method=\"post\">\n";
		print "<input type=hidden name=mode value=\"usr_edt\">\n";
		print "<input type=hidden name=action value=\"edit\">\n";
		print "<input type=hidden name=pwd value=\"$in{'pwd'}\">\n";
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
	# 返信時
	} elsif ($mode eq 'msgview') {
		$wrap='soft';
		print "<hr width=\"95%\"><a name=\"msg\"></a>\n";
		print "<b style=\"text-indent:18\">- 返信フォーム</b>\n";
		print "（この記事に返信する場合は下記フォームから投稿して下さい）<br>\n";
		print "<form action=\"$regist\" method=\"post\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"form\">\n";
		print "<input type=\"hidden\" name=\"page\" value=\"$page\">\n";
		print "<input type=\"hidden\" name=\"action\" value=\"res_msg\">\n";
		print "<input type=\"hidden\" name=\"no\" value=\"$in{'no'}\">\n";
		print "<input type=\"hidden\" name=\"oya\" value=\"$in{'oya'}\">\n";
	# 新規時
	} else {
		$wrap = 'soft';
		print "<hr width=\"95%\"><p><a name=\"msg\"></a><div align=\"center\">\n";
		print "<b><big>メッセージをどうぞ・・</big></b></a></div>\n";
		print "<P><form action=\"$regist\" method=\"post\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"form\">\n";
		print "<input type=\"hidden\" name=\"page\" value=\"$page\">\n";
		print "<input type=\"hidden\" name=\"no\" value=\"new\">\n";
	}

	print "<blockquote><table border=\"0\" cellspacing=\"0\" cellpadding=\"1\">\n";
	print "<tr><td><b>おなまえ</b></td>";
	print "<td><input type=\"text\" name=\"name\" size=\"28\" value=\"$cname\"></td></tr>\n";
	print "<tr><td><b>Ｅメール</b></td>";
	print "<td><input type=\"text\" name=\"email\" size=\"28\" value=\"$cmail\"> ";
	print "<select name=\"smail\">\n";

	@sm = ('表示', '非表示');
	if ($csmail eq "") { $csmail=0; }
	foreach (0, 1) {
		if ($csmail == $_) {
			print "<option value=\"$_\" selected>$sm[$_]\n";
		} else {
			print "<option value=\"$_\">$sm[$_]\n";
		}
	}

 	print "</select></td></tr>\n";
	print "<tr><td><b>タイトル</b></td>";
	print "<td><input type=\"text\" name=\"sub\" size=\"38\" value=\"$res_sub\"></td></tr>\n";
	print "<tr><td colspan=\"2\"><b>メッセージ</b>&nbsp;&nbsp;&nbsp;";

	@w1 = ('手動改行', '強制改行', '図表モード');
	@w2 = ('soft', 'hard', 'pre');
	foreach (0 .. 2) {
		if ($wrap eq $w2[$_]) {
			print "<input type=\"radio\" name=\"wrap\" value=\"$w2[$_]\" checked>$w1[$_]\n";
		} else {
			print "<input type=\"radio\" name=\"wrap\" value=\"$w2[$_]\">$w1[$_]\n";
		}
	}

	# プレビューのチェック
	if ($cpv eq "on") { $checked = "checked"; }

	print "<br><textarea name=\"message\" rows=\"10\" cols=\"62\">$res_msg</textarea>";
	print "</td></tr><tr><td><b>参照先</b></td>";
	print "<td><input type=\"text\" name=\"url\" size=\"58\" value=\"$curl\"></td></tr>\n";

	if ($_[0] eq "edt") {
		print "<tr><td></td><td><input type=\"submit\" value=\" 記事を修正する \"></td>\n";
		print "</tr></table></form></blockquote>\n";
	} else {
		print <<"EOM";
<tr>
  <td><b>暗証キー</b></td>
  <td><input type="password" name="pwd" size="8" value="$cpwd" maxlength=8>
	(英数字で8文字以内)</td>
</tr>
<tr>
  <td></td>
  <td><input type="submit" value=" 記事を投稿する ">
	 &nbsp; <input type="checkbox" name="pview" value="on" $checked>プレビュー</td>
</tr>
</table>
</form>
</blockquote>
<hr width="95%">
<div align="center">
<form action="$regist" method="post">
<input type="hidden" name="page" value="$page">
<font color="$sub_color">
- 以下のフォームから自分の投稿記事を修正・削除することができます -</font><br>
処理 <select name="mode">
<option value="usr_edt">修正
<option value="usr_del">削除
</select>
記事No <input type="text" name="no" size="4" style="ime-mode:inactive">
暗証キー <input type="password" name="pwd" size="6">
<input type="submit" value="送信"></form>
<hr width="95%"></div>
EOM
	}
}

#---------------------------------------
#  クッキー取得
#---------------------------------------
sub get_cookie {
	local($key, $val, *cook);

	# クッキー情報取得
	$cook = $ENV{'HTTP_COOKIE'};

	# 該当IDを取り出す
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# データをURLデコードして復元
	foreach ( split(/<>/, $cook{'WFORUM'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("H2", $1)/eg;

		push(@cook,$_);
	}
	return (@cook);
}

#---------------------------------------
#  クッキー発行
#---------------------------------------
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 国際標準時を定義
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# 保存データをURLエンコード
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# 格納
	print "Set-Cookie: WFORUM=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  禁止ワードチェック
#-------------------------------------------------
sub no_wd {
	local($flg);
	foreach ( split(/,/, $no_wd) ) {
		if (index("$in{'name'} $in{'sub'} $in{'message'}",$_) >= 0) {
			$flg = 1; last;
		}
	}
	if ($flg) { &error("禁止ワードが含まれています"); }
}

#-------------------------------------------------
#  日本語チェック
#-------------------------------------------------
sub jp_wd {
	local($sub, $com, $mat1, $mat2, $code1, $code2);
	$sub = $in{'sub'};
	$com = $in{'message'};
	if ($sub) {
		($mat1, $code1) = &jcode'getcode(*sub);
	}
	($mat2, $code2) = &jcode'getcode(*com);
	if ($code1 ne 'sjis' && $code2 ne 'sjis') {
		&error("題名又はコメントに日本語が含まれていません");
	}
}

#-------------------------------------------------
#  URL個数チェック
#-------------------------------------------------
sub urlnum {
	local($com) = $in{'message'};
	local($num) = ($com =~ s|(https?://)|$1|ig);
	if ($num > $urlnum) {
		&error("コメント中のURLアドレスは最大$urlnum個までです");
	}
}


1;

