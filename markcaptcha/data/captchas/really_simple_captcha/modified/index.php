<?php
require("really-simple-captcha.php");

$captcha_instance = new ReallySimpleCaptcha();
$word = $captcha_instance->generate_random_word();
$captcha_instance->generate_image("", $word );

$total = 1502;

for($i = 1; $i<= $total; $i++){
  $files = glob("tmp\\" . "*");
  if (count($files) == $total){
    echo "CAPTCHA generation completed.";
    break;
  }
  $captcha_instance = new ReallySimpleCaptcha();
  $word = $captcha_instance->generate_random_word();
  $captcha_instance->generate_image("", $word );
}
?>
