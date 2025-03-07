<?php

    error_reporting(0);
    ob_end_flush();

    function win() {
        # read flag.txt
        $flag = file_get_contents('./flag.txt');
        echo "You win! Here's your flag: $flag";
    }

    $list = str_split("xylkwbfztnjrqahvgmuopdicse");
    for ($index = 0; $index < count($list); $index++) {
        $tmp = chr($index + ord("a"));
        $$tmp = $list[$index];
    }

    print("Password: ");
    $password = readline();

    $hashed_password = '';
    for ($index = 0; $index <= 20; $index++){
        $var = $password[$index];

        switch ($index){
            case 14: $var = $$$$$$$$var;
            case 20: $var = $$$$var;
            case  0: $var = $$$$$$$$$var;
            case 13: $var = $$$var;
            case 17: $var = $$$$var;
            case  1: $var = $$$$$$$$var;
            case 16: $var = $$var;
            case 15: $var = $$$$$var;
            case  8: $var = $$$$$$$$$$$$$$$$var;
            case  6: $var = $$$var;
            case 12: $var = $$var;
            case  4: $var = $$$$$$$$$$$var;
            case  3: $var = $$$$$$$var;
            case 19: $var = $$var;
            case  2: $var = $$$var;
            case 11: $var = $$$$$$$$$var;
            case  9: $var = $$$$$$$$$$$$$$$$$$$$$$$$var;
            case 18: $var = $$$$$$var;
            case  5: $var = $$$$$$$$$$$$$var;
            case 10: $var = $$$var;
            default: $var = $$$$$$$$var;
        }

        $hashed_password .= $var;
    }

    $list1 = str_split("nuydhkeoxzlirpmcjfbgwvtasq");
    $list2 = str_split("uydhkeoxzlirpmcjfbgwvtasqn");
    for ($index = 0; $index < count($list1); $index++) {
        $tmp  = $list1[$index];
        $$tmp = $list2[$index];
    }

    if (
            ($$$$$$$$$$$$$i . $$$$$$$$$$$$$$$$$k . $$$$$$$$$$$$$$$$$$$$$$$$m . $$$$$$$$$$$$$$$$$$$$$$$$f . $$$$$$$$e . $$$l)
            ($hashed_password, "cszsoicvytzneneqakgvw")
            == ($$$$$$$$q . $$$$$$$$$$$$$$$$$v . $$$$$$$$$$$b)($$$$$$t) - ($$$$$$$$q . $$$$$$$$$$$$$$$$$v . $$$$$$$$$$$b)($$$h) + ($$$$$$$$q . $$$$$$$$$$$$$$$$$v . $$$$$$$$$$$b)($$$$$$$$$$s) - ($$$$$$$$q . $$$$$$$$$$$$$$$$$v . $$$$$$$$$$$b)($$$$f) + ($$$$$$$$q . $$$$$$$$$$$$$$$$$v . $$$$$$$$$$$b)($$$$$$$$$$t) - ($$$$$$$$q . $$$$$$$$$$$$$$$$$v . $$$$$$$$$$$b)($$$$$w)
        ){
        ($$$$$$$$$$$$$$$$a . $$$z . $$$$$$$$$$$$$$$$$$$$$j . $$$$$$w . $$$$$$$$$$$$$$$$e . $$$$$$$$$$$$$$$$$$$$$$$$$$f)($$$$$$$$$$$$$$$$$$$$$$$u . $$$$$t . $$$$$$$$$$$$$$$$$s . $$$$$$$$$$$$$$u . $$$$$$$$$$$$$$$$$$$$$$$$$$e . $$$$$g . $$$$$$b . "!\n");
        win();
    }

?>
