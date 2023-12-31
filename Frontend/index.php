<?php
session_start();

if (isset($_SESSION['username'])) {
    header("location: chat.php");
    exit;
}

$loginFailed = isset($_GET['login']) && $_GET['login'] === 'failed';
?>

<!-- 登入介面模板: https://github.com/HQEasy/login-page-template -->
<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>案件查詢-登入系統</title>
    <link rel="stylesheet" href="css/tailwind.min.css">
    <style>
        .dowebok .weixin, .dowebok .weibo {
            display: inline-block;
            width: 32px;
            height: 32px;
            background-size: cover;
        }

        .dowebok .weixin {
            background-image: url(images/weixin.png);
        }

        .dowebok .weibo {
            background-image: url(images/weibo.png);
        }
    </style>
</head>

<body class="min-h-screen bg-gray-100 text-gray-900 flex justify-center dowebok">
    <div class="max-w-screen-xl m-0 sm:m-20 bg-white shadow sm:rounded-lg flex justify-center flex-1">
        <div class="lg:w-1/2 xl:w-5/12 p-6 sm:p-12">
            <div class="mt-12 flex flex-col items-center">
                <h1 class="text-2xl xl:text-3xl font-extrabold">用戶登入</h1>
                <div class="w-full flex-1 mt-8">

                    <div class="flex flex-col items-center">
                        <button class="w-full max-w-xs font-bold shadow-sm rounded-lg py-3 bg-indigo-100 text-gray-800 flex items-center justify-center ease-in-out focus:outline-none hover:shadow focus:shadow-sm focus:shadow-outline">
                            <div class="weixin"></div>
                            <span class="ml-4">使用微信登入</span>
                        </button>
                        <button class="w-full max-w-xs font-bold shadow-sm rounded-lg py-3 bg-indigo-100 text-gray-800 flex items-center justify-center ease-in-out focus:outline-none hover:shadow focus:shadow-sm focus:shadow-outline mt-5">
                            <div class="weibo"></div>
                            <span class="ml-4">使用微博登入</span>
                        </button>
                    </div>

                    <div class="my-12 border-b text-center">
                        <div class="leading-none px-2 inline-block text-sm text-gray-600 tracking-wide font-medium bg-white transform translate-y-1/2">或者使用帳號密碼登入</div>
                    </div>

                    <div class="mx-auto max-w-xs">
    <?php if ($loginFailed): ?>
        <div class="alert alert-danger" role="alert">
            Invalid username or password.
        </div>
    <?php endif; ?>

    <form action="authenticate.php" method="post" autocomplete="off">
        <input class="w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white" type="text" placeholder="帳號" name="username" required />
        <input class="w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white mt-5" type="password" placeholder="密碼" name="password" required />
        <button type="submit" class="mt-5 tracking-wide font-semibold bg-indigo-500 text-gray-100 w-full py-4 rounded-lg hover:bg-indigo-700 ease-in-out flex items-center justify-center focus:shadow-outline focus:outline-none">
            <span class="ml-3">登 入</span>
        </button>
    </form>
    <p class="mt-6 text-xs text-gray-600 text-center">我同意並遵守服務協議</p>
</div>
                </div>
            </div>
        </div>
        <div class="flex-1 bg-indigo-100 text-center hidden lg:flex">
            <div class="m-12 xl:m-16 w-full bg-contain bg-center bg-no-repeat" style="background-image: url('images/dowebok.svg');"></div>
        </div>
    </div>
</body>
</html>