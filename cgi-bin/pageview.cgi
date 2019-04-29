#!/usr/local/bin/perl

# ----------------------------------------------------------------------------------
# Page Counter View Version 1.10（カウント表示用）
#
# Script written by Nishiyama(CGIダウンロード)
# This script is free
# HomePage http://www.cgi-down.com/
# E-Mail webmaster@cgi-down.com
# (1999/10/22-2000/08/28)
# 改変履歴
#
# 2000-08-28 V1.10 タイトル色を指定しても色が変わらないバグ修正。ロック機能追加。
# 1999-10-23 V1.00 正式リリース
#
# 再配布禁止（利用規定をお読み下さい）
# 使用されたらメールをいただけると光栄です。
# 設置等不明な点は、サポート掲示板へお願いします。
# ----------------------------------------------------------------------------------
#
# **********************************************************************************
#                       オプション設定　↓ここから
# **********************************************************************************
# -------------------------------------------------------
#      管理者の設定（管理者とは、あなたです）※必須
# -------------------------------------------------------

$master_name = 'user';            # 管理者の名前
$master_email = 'user@**.ne.jp';  # 管理人のメールアドレス
$master_pass = 'abc';             # 管理人のパスワード
$master_url = 'http://www....';   # 管理者のURL（トップページ）

# -------------------------------------------------------
#      ファイル関連設定　※必須
# -------------------------------------------------------

$jcode    = './jcode.pl';         # jcode.plの位置
$cgifile  = './pageview.cgi';     # このCGIの位置
$datefile = './dat/pagecon.dat';      # データー記録ファイル(pagecon.cgiと同じにする)
$gurafu   = './gurafu.gif';       # グラフ用GIF画像の位置

# -------------------------------------------------------
#      その他必要に応じて設定する項目
# -------------------------------------------------------

$title ='人気ページ';             # タイトル
$size  = '300';                   # グラフのサイズを決める係数です。
                                  # グラフの幅があまり大きくなりすぎたときは数値を減らして下さい。
# ---------- 各色設定部 --------------
$title_color   = '#4682b4';       # このCGIのタイトルの文字色
$table_color   = '#E6E6FA';       # テーブルカラー
# ---------- body色設定部 ------------
$background    = '';              # バック画像を使用するときは「''」の間にhttp://～
                                  # 又は、相対パスで画像の位置をお書き下さい。
                                  # 使用しないときは、そのままでOK。

$bgcolor       = '#ffffff';       # 背景色(バック画像をお使いの場合は無効となります)
$text_color    = '#000000';       # 通常文字色
$link_color    = '#3366cc';       # LINKの文字色
$alink_color   = '#ff69b4';       # ALINKの文字色
$vlink_color   = '#c71585';       # VLINKの文字色

# **********************************************************************************
#                     オプション設定終わり　↑ここまで
# ----------------------------------------------------------------------------------
# これ以降書き換えをする場合は、個人の責任で行って下さい。
# **********************************************************************************
# [メイン処理]
if (!(-r $jcode)) { &error(bat_jcode); }
require $jcode;
@DATE = &read_file($datefile);
&read_form;
&html_view;
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [ヘッダー部分]
sub html_header {
  print "Content-type: text/html\n\n";
  print "<HTML><HEAD><TITLE>$title</TITLE></HEAD>\n";
  if ($background eq '') {
    print "<BODY BGCOLOR=$bgcolor TEXT=$text_color LINK=$link_color ALINK=$alink_color VLINK=$vlink_color>\n";
  } else {
    print "<BODY BACKGROUND=$background BGCOLOR=$bgcolor TEXT=$text_color LINK=$link_color ALINK=$alink_color VLINK=$vlink_color>\n";
  }
  print "<DIV ALIGN=center><FONT SIZE=5 color=\"$title_color\"><B>$title</B></FONT></DIV>\n\n";
  print "<DIV ALIGN=right>★　<A HREF=\"$master_url\" TARGET=\"_top\">HOME</A>　★</DIV>\n";

  print "<HR>\n\n";
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [フッター部分]
sub html_footer {
  print "<DIV ALIGN=right>[管理者：<A HREF=\"mailto:$master_email\">$master_name</A>]</DIV>\n";
  print "<HR>\n";

## 著作権表示（必ず表示して下さい）
  print "<DIV ALIGN=right>Page Counter Version 1.10 [<A HREF=\"http://www.cgi-down.com/\">CGIダウンロード</A>]</DIV>\n";

  print "</BODY></HTML>\n";
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [ＴＯＰ表示]
sub html_view {
  &html_header;

# 連想配列に代入
  $num = 0;
  foreach $lines (@DATE) {
    local($date,$page,$name,$count,$addr) = split(/☆|★/,$lines);
    local($day,$hr) = split(/ /,$date);
    $totle = $totle + $count;
    $num++;
    $day{$num} = $day;
    $page{$num} = $page;
    $name{$num} = $name;
    $count{$num} = $count;
    $addr{$num} = $addr;
  }

  print "<CENTER>\n";
  print "<TABLE BORDER=1 bgcolor=$table_color>\n";
  print "<TR>\n";
  print "<TD ALIGN=center><B>順位</B></TD>\n";
  print "<TD ALIGN=center><B>アクセス日</B></TD>\n";
  print "<TD ALIGN=center><B>ページ名</B></TD>\n";
  print "<TD ALIGN=center><B>アクセス数</B></TD>\n";
  print "<TD ALIGN=center><B>グラフ</B></TD>\n";
  print "</TR>\n\n";

# ダウンロード数の多い順位ソートし表示する。
  $ranking = 0;
  foreach (sort { ($count{$b} <=> $count{$a}) || ($a cmp $b)} keys(%count)) {
    $ranking++;
    $part = int($count{$_} / $totle * $size);
    print "<TR>\n";
    print "<TD ALIGN=right><B>$ranking</B></TD>\n";
    print "<TD ALIGN=right><B>$day{$_}</B></TD>\n";
    print "<TD ALIGN=center><A HREF=\"$page{$_}\"><B>$name{$_}</B></A></TD>\n";
    print "<TD ALIGN=right><B>$count{$_}</B></TD>\n";
    print "<TD ALIGN=left><img src=$gurafu width=$part height=20></TD>\n";
    print "</TR>\n\n";
  }
  print "<TR>\n";
  print "<TD ALIGN=center><B>合計</B></TD>\n";
  print "<TD ALIGN=center><B>　</B></TD>\n";
  print "<TD ALIGN=center><B>　</B></TD>\n";
  print "<TD ALIGN=right><B>$totle</B></TD>\n";
  print "<TD ALIGN=center><B>　</B></TD>\n";
  print "</TR>\n\n";
  print "</TABLE>\n";
  print "</CENTER>\n\n";
  &html_footer;
  exit;
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [記録ファイルの読み込み]
sub read_file {
  local($date_file) = $_[0];
  if (!open(IN,$date_file)) { &error(bat_file); }
  local(@date_files) = <IN>;
  close(IN);
  return @date_files;
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [フォームデータを取得し、文字コード統一]
sub read_form {
  local($pair,$form_date);
  if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $form_date, $ENV{'CONTENT_LENGTH'}); }
  else { $form_date = $ENV{'QUERY_STRING'}; }
  local(@pairs) = split(/&/,$form_date);
  foreach $pair (@pairs) {
    local($name,$value) = split(/=/,$pair);
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
    &jcode'convert(*value,'sjis');
    $FORM{$name} = $value;
  }
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [エラー関連]
sub error {
  $error = $_[0];
  if ($error eq "bat_jcode") { $error_message = 'jcode.pl が見つかりません'; }
  elsif ($error eq "bat_code") { $error_message = 'サポートされていない文字コードです'; }
  elsif ($error eq "bat_file") { $error_message = 'データファイルがありません'; }

  print "Content-type: text/html\n\n";
  print "<html><head><title>$error_message</title></head>\n";
  print "<BODY bgcolor=ffffff text=000000>\n";
  print "<BR><BR><BR><CENTER>\n\n";
  print "<TABLE BORDER=0>\n";
  print "<TR><TD BGCOLOR=#FFCCCC WIDTH=70 ALIGN=center>\n";
  print "<FONT SIZE=4><B>エラー</B></FONT></TD>\n\n";
  print "<TD BGCOLOR=#FFCC99 WIDTH=500 ALIGN=center>\n";
  print "<FONT SIZE=4><B>$error_message</B></FONT></TD></TR>\n";
  print "</CENTER>\n\n";
  print "</BODY></HTML>\n";
  exit;
}
