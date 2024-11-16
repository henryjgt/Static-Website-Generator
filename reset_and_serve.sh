rm -rfv ./public/*

cat >> ./public/index.html << 'END_HTML'
<html>
<head>
    <title>Why Frontend Development Sucks</title>
</head>
<body>
    <h1>Front-end Development is the Worst</h1>
    <p>
        Look, front-end development is for script kiddies and soydevs who can't handle the real programming. I mean,
        it's just a bunch of divs and spans, right? And css??? It's like, "Oh, I want this to be red, but not thaaaaat
        red." What a joke.
    </p>
    <p>
        Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not
        Windows. They use Vim, not VS Code. They use C, not HTML. Come to the
        <a href="https://www.boot.dev">backend</a>, where the real programming
        happens.
    </p>
</body>
</html>
END_HTML

cat >> ./public/styles.css << 'END_CSS'
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background-color: #1f1f23;
}
body {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}
h1 {
    color: #ffffff;
    margin-bottom: 20px;
}
p {
    color: #999999;
    margin-bottom: 20px;
}
a {
    color: #6568ff;
}
END_CSS

cd ./public && python3 -m http.server 8888