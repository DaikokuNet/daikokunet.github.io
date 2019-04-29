#!/usr/local/bin/perl

# ----------------------------------------------------------------------------------
# Page Counter Version 1.10（カウント用）
#
# Script written by Nishiyama(CGIダウンロード)
# This script is free
# HomePage http://www.cgi-down.com/
# E-Mail webmaster@cgi-down.com
# (1999/10/22-2000/08/28)
# 改変履歴
#
# 2000-08-28 V1.10 タイトル色を指定しても色が変わらないバグ修正、ロック機能追加。
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
#      ファイル関連設定　※必須
# -------------------------------------------------------

$jcode    = './jcode.pl';                   # jcode.plの位置
$datefile = './dat/pagecon.dat';                # データー記録ファイル
$lock     = '1';                            # ロック機能(1:使用する　　0:使用しない)
$lockfile = './lock/pagecon.lock';          # ロックファイル名(必要以外変更しないで下さい)

# **********************************************************************************
#                     オプション設定終わり　↑ここまで
# ----------------------------------------------------------------------------------
# これ以降書き換えをする場合は、個人の責任で行って下さい。
# **********************************************************************************
# [メイン処理]
if (!(-r $jcode)) { &error(bat_jcode); }
require $jcode;
&read_form;
@DATE = &read_file($datefile);
&registry;

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [ファイルに記録]
sub registry {
  $n_page = $FORM{'page'};
  $n_name = $FORM{'name'};

# IPアドレスを取得
  $n_addr = $ENV{'REMOTE_ADDR'};

# 現在時間の取得
  ($new_date) = &time;

  $m = 0;
  foreach $lines (@DATE) {
    local($date,$page,$name,$count,$addr) = split(/☆|★/,$lines);
    if ($n_name eq $name) {
      $m = 1;
      $count++;
      $lines = "$new_date☆$n_page☆$n_name☆$count☆$n_addr★\n";
    }
    push(@NEW,$lines);
  }

# 既存の場合
  if ($lock) {
    foreach $i ( 1, 2, 3, 4, 5, 6 ) {
      if (mkdir("$lockfile", 0755)) {
        last;
      } elsif ($i == 1) {
        local($mtime) = (stat($lockfile))[9];
        if ($mtime < time() - 600) {
          rmdir($lockfile);
        }
      } elsif ($i < 6) {
        sleep(1);
      } else {
        &error(28);   # 6秒待ってもロックされていれば混雑中
      }
    }
  }
  if ($m == 1) {
    if (!open(OUT, ">$datefile")) { &error(bat_file); }
    print OUT @NEW;
    close (OUT);
  }

# 新規の場合
  elsif ($m == 0) {
    if (!open(OUT, ">>$datefile")) { &error(bat_file); }
    $count = 1;
    print OUT "$new_date☆$n_page☆$n_name☆$count☆$n_addr★\n";
    close (OUT);
  }
  if ($lock) {
    rmdir($lockfile);   # 書き込みが終わってロック解除
  }
  print "Location: $n_page\n\n";
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
    $value =~ s/"/&quot\;/g;
    $value =~ s/<>/&gt\;&lt\;/g;
    &jcode'convert(*value,'sjis');
    $FORM{$name} = $value;
  }
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [現在時刻を取得]
sub time{
  $ENV{'TZ'} = "JST-9";
  ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime();
  $year = $year + 1900;
  $mon = sprintf("%.2d",$mon +1);
  $mday = sprintf("%.2d",$mday);
  $hour = sprintf("%.2d",$hour);
  $min = sprintf("%.2d",$min);
  $sec = sprintf("%.2d",$sec);
# 曜日を日本語化
  @week = ('日','月','火','水','木','金','土');
  $wday = $week[$wday];
  local($date) = "$year年$mon月$mday日($wday) $hour時$min分$sec秒";
  return ($date);
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
