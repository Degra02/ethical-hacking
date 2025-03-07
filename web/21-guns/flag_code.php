<?php
    $f1 = "UniTN{One_21"; $f2="__Guns__"; $f3="_Chars}";
?>

<?php
ini_set('display_errors', 'on');
ini_set('error_reporting', E_ALL ^ E_DEPRECATED);

if (isset ($_GET['source'])) {
    show_source(__FILE__);
    die();
}


if (isset ($_GET['code']) && is_string ($_GET['code'])) {
            $code = substr ($_GET['code'], 0, 21);
} else {
            $code = "'I hate PHP'";
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Little RCE</title>

</head>
    <body>

        <h1>21 Guns <small>Green Day???</small></h1>


        <form method="get">

            <label for="code">Code:</label>
            <input type="text" id="code" name="code" value="<?php echo htmlspecialchars ($code);?>" required maxlength=25>
            <button type="submit">Execute!</button>
        </form>

        <div>
<br>
<pre>

<?php
class A {
    public $pub;
    protected $pro ;
    private $pri;

    function __construct($pub, $pro, $pri) {
        $this->pub = $pub;
        $this->pro = $pro;
        $this->pri = $pri;
    }
}

include 'flag.php';
$a = new A($f1, $f2, $f3);

unset($f1);
unset($f2);
unset($f3);

$funcs_internal = get_defined_functions()['internal'];


unset ($funcs_internal[array_search('strlen', $funcs_internal)]);
unset ($funcs_internal[array_search('print', $funcs_internal)]);
unset ($funcs_internal[array_search('strcmp', $funcs_internal)]);
unset ($funcs_internal[array_search('strncmp', $funcs_internal)]);

$funcs_extra = array ('eval', 'include', 'require', 'function');
$funny_chars = array ('\.', '\+', '-', '"', ';', '`', '\[', '\]');
$variables = array ('_GET', '_POST', '_COOKIE', '_REQUEST', '_SERVER', '_FILES', '_ENV', 'HTTP_ENV_VARS', '_SESSION', 'GLOBALS');

$blacklist = array_merge($funcs_internal, $funcs_extra, $funny_chars, $variables);

$insecure = false;
foreach ($blacklist as $blacklisted) {
    if (preg_match ('/' . $blacklisted . '/im', $code)) {
        $insecure = true;
        break;
    }
}

if ($insecure) {
    echo 'Insecure code detected!';
} else {
    eval ("echo $code;");
}
?>
</pre>
            </div>
        </div>
</div>
</body>
</html>
</html></pre>
            </div>
        </div>
</div>
</body>
</html>
