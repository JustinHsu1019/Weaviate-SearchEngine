<?php
require_once 'vendor/autoload.php';
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

session_start();

if (!isset($_GET['token'])) {
    header("location: index.php");
    exit;
}

try {
    $decoded = JWT::decode($_GET['token'], new Key('your_secret_key', 'HS256'));
    $username = $decoded->username;

    if ($username !== $hardcodedUsername) {
        header("location: index.php?login=failed");
        exit;
    }
} catch (\Exception $e) {
    header("location: index.php?login=failed");
    exit;
}
?>

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>金管會裁罰案件查詢系統</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
        body {
            background-color: #f4f4f4;
            margin: 0;
            padding-bottom: 70px;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
            height: 95vh;
            padding: 10px 0;
        }

        #chatWindow {
            flex-grow: 1;
            overflow-y: auto;
            border: 1px solid #ccc;
            margin-bottom: 10px;
            padding: 10px;
            background-color: #fff;
        }

        *::-webkit-scrollbar {
            width: 8px;
        }

        *::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        *::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }

        *::-webkit-scrollbar-thumb:hover {
            background: #555;
        }

        #messageInput {
            font-size: 16px;
        }

        .input-group {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #fff;
        }

        .input-group-prepend .btn {
            padding: 10px 15px;
            font-size: 18px;
        }

        .form-control {
            padding: 10px;
            font-size: 18px;
            height: auto;
        }

        @media (max-width: 768px) {

            .input-group-prepend .btn,
            .form-control {
                padding: 12px 20px;
                font-size: 20px;
            }
        }

        .input-group .btn {
            border-top-right-radius: 0;
            border-bottom-right-radius: 0;
        }
    </style>
</head>

<body>
    <div class="container-fluid chat-container">
        <h2 class="text-center">金管會裁罰案件查詢系統</h2>
        <div id="chatWindow">
            <!-- Messages will appear here -->
        </div>
        <div class="input-group">
            <div class="input-group-prepend">
                <button onclick="sendMessage()" class="btn btn-primary">Send</button>
            </div>
            <input type="text" id="messageInput" class="form-control" placeholder="Type a message...">
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script>
        document.getElementById("messageInput").addEventListener("keyup", function (event) {
            if (event.key === "Enter") {
                sendMessage();
            }
        });

        function sendMessage() {
            var message = document.getElementById("messageInput").value;
            if (message.trim() === '') {
                return;
            }

            var chatWindow = document.getElementById("chatWindow");
            var newMessageDiv = document.createElement("div");
            newMessageDiv.classList.add("message", "you");
            newMessageDiv.textContent = "You: " + message;
            chatWindow.appendChild(newMessageDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;
            document.getElementById("messageInput").value = '';

            $.ajax({
                url: 'YOUR_BACKEND_URL/chat',
                type: 'POST',
                data: { mess: message },
                success: function (response) {
                    var newResponseDiv = document.createElement("div");
                    newResponseDiv.classList.add("message");
                    newResponseDiv.textContent = "Bot: " + response;
                    chatWindow.appendChild(newResponseDiv);
                    chatWindow.scrollTop = chatWindow.scrollHeight;
                },
                error: function () {
                    console.error("Error sending message");
                }
            });
        }
    </script>
</body>

</html>