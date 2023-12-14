<?php
require_once 'vendor/autoload.php';
use Firebase\JWT\JWT;

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
        $payload = [
            "username" => $username
        ];

        $jwt = JWT::encode($payload, 'your_secret_key', 'HS256');
        header("location: chat.php?token=".$jwt);
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
