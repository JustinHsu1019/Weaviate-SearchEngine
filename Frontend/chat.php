<?php
session_start();

if (!isset($_SESSION['username'])) {
    header("location: index.php");
    exit;
}

?>

<!DOCTYPE html>
<html>

<head>
    <title>金管會裁罰案件查詢系統</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
        body {
            background-color: #f4f4f4;
        }

        #chatWindow {
            flex-grow: 1;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            background-color: #fff;
            margin-bottom: 10px;
        }

        .message {
            margin: 5px;
            padding: 10px;
            background-color: #e2e2e2;
            border-radius: 5px;
        }

        .message.you {
            text-align: right;
        }

        #chatWindow::-webkit-scrollbar {
            width: 8px;
        }

        #chatWindow::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        #chatWindow::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }

        #chatWindow::-webkit-scrollbar-thumb:hover {
            background: #555;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
            height: 95vh;
        }

        .input-group {
            width: 100%;
        }
    </style>
</head>

<body>
    <div class="container my-4 chat-container">
        <h2 class="text-center">金管會裁罰案件查詢系統</h2>
        <div id="chatWindow">
            <!-- Messages will appear here -->
        </div>
        <div class="input-group">
            <input type="text" id="messageInput" class="form-control" placeholder="Type a message...">
            <div class="input-group-append">
                <button onclick="sendMessage()" class="btn btn-primary">Send</button>
            </div>
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
