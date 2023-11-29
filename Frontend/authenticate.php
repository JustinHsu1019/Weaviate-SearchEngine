<?php
// Hardcoded credentials
$hardcodedUsername = "YOUR_USERNAME";
$hardcodedPassword = "YOUR_PASSWORD";

session_start();

$username = "";
$password = "";

if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if ($username === $hardcodedUsername && $password === $hardcodedPassword) {
        $_SESSION['username'] = $username;
        header("location: chat.php");
        exit;
    } else {
        header("location: index.php?login=failed");
        exit;
    }
} else {
    header("location: index.php");
    exit;
}
?>
