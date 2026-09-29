<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ÖSYM Yazım Hızı & Pratik Stüdyosu</title>
    <style>
        body {
            background-color: #13111c;
            color: #646669;
            font-family: 'Courier New', monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }

        .container {
            width: 850px;
            max-width: 90%;
            text-align: center;
        }

        /* Üst Menü & Süre Butonları */
        .header-menu {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1a1625;
            padding: 10px 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid #2c2738;
        }

        .time-modes button {
            background: none;
            border: none;
            color: #646669;
            font-family: inherit;
            font-size: 16px;
            cursor: pointer;
            padding: 5px 10px;
            margin: 0 4px;
            border-radius: 6px;
            transition: 0.2s;
        }

        .time-modes button.active, .time-modes button:hover {
            color: #e2b714;
        }

        /* İstatistik Kartları */
        .stats-bar {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }

        .stat-box {
            background: #1a1625;
            padding: 15px 25px;
            border-radius: 10px;
            border: 1px solid #2c2738;
            flex: 1;
            text-align: left;
        }

        .stat-box .title {
            font-size: 13px;
            color: #646669;
        }

        .stat-box .value {
            font-size: 28px;
            color: #d1d0c5;
            font-weight: bold;
        }

        /* Kelime Alanı (Coderspace Tarzı) */
        .word-display {
            font-size: 26px;
            line-height: 1.8;
            height: 140px;
            overflow: hidden;
            text-align: left;
            position: relative;
            background: #1a1625;
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #2c2738;
            user-select: none;
        }

        .word {
            display: inline-block;
            margin-right: 12px;
            position: relative;
        }

        .letter {
            border-bottom: 2px solid transparent;
        }

        .letter.correct {
            color: #d1d0c5;
        }

        .letter.incorrect {
            color: #ca4754;
            border-bottom: 2px solid #ca4754;
        }

        /* Gizli Input (Klavyeden yazılanları yakalamak için) */
        #hidden-input {
            position: absolute;
            opacity: 0;
            pointer-events: none;
        }

        /* Yeniden Başlat Butonu */
        .restart-btn {
            background: #2c2738;
            border: none;
            color: #d1d0c5;
            padding: 10px 20px;
            font-family: inherit;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 25px;
            transition: 0.2s;
        }

        .restart-btn:hover {
            background: #e2b714;
            color: #13111c;
        }
    </style>
</head>
<body onclick="document.getElementById('hidden-input').focus()">

    <div class="container">
        <!-- Üst Menü -->
        <div class="header-menu">
            <div style="color: #d1d0c5; font-weight: bold;">⚡ ÖSYM Yazım Hızı Pratiği</div>
            <div class="time-modes">
                <button onclick="setDuration(15)" id="btn-15">15 sn</button>
                <button onclick="setDuration(30)" id="btn-30" class="active">30 sn</button>
                <button onclick="setDuration(60)" id="btn-60">60 sn</button>
                <button onclick="setDuration(120)" id="btn-120">120 sn</button>
            </div>
        </div>

        <!-- İstatistikler -->
        <div class="stats-bar">
            <div class="stat-box">
                <div class="title">Süre</div>
                <div class="value" id="timer">30</div>
            </div>
            <div class="stat-box">
                <div class="title">WPM (Hız)</div>
                <div class="value" id="wpm">0</div>
            </div>
            <div class="stat-box">
                <div class="title">Doğruluk</div>
                <div class="value" id="accuracy">100%</div>
            </div>
        </div>

        <!-- Kelime Havuzu Alanı -->
        <div class="word-display" id="word-display"></div>

        <!-- Görünmeyen Klavye Okuyucu -->
        <input type="text" id="hidden-input" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">

        <br>
        <button class="restart-btn" onclick="startGame()">🔄 Yeniden Başlat</button>
    </div>

    <script>
        // ÖSYM'nin en çok karıştırılan kelimelerinin DOĞRU halleri
        const osymWords = [
            "yalnız", "yanlış", "herkes", "unvan", "orijinal", 
            "kılavuz", "şoför", "stajyer", "laboratuvar", "doküman", 
            "palyaço", "akaryakıt", "birdenbire", "birkaç", "hapishane", 
            "karpuz", "komite", "unutkan", "özgün", "esrar", 
            "kirpik", "poğaça", "savrulmak", "kolej", "dereotu", 
            "başyapıt", "taşeron", "mütevazi", "akıbet", "özveri",
            "tespit", "sezgi", "makine", "unutulmaz", "öngörü"
        ];

        let duration = 30;
        let timeLeft = duration;
        let timerInterval = null;
        let isPlaying = false;
        let words = [];
        let wordIndex = 0;
        let charIndex = 0;
        let correctChars = 0;
        let totalTypedChars = 0;

        const wordDisplay = document.getElementById('word-display');
        const hiddenInput = document.getElementById('hidden-input');
        const timerDisplay = document.getElementById('timer');
        const wpmDisplay = document.getElementById('wpm');
        const accuracyDisplay = document.getElementById('accuracy');

        function shuffle(array) {
            return array.sort(() => Math.random() - 0.5);
        }

        function startGame() {
            clearInterval(timerInterval);
            isPlaying = false;
            timeLeft = duration;
            timerDisplay.innerText = timeLeft;
            wpmDisplay.innerText = "0";
            accuracyDisplay.innerText = "100%";
            wordIndex = 0;
            charIndex = 0;
            correctChars = 0;
            totalTypedChars = 0;

            words = shuffle([...osymWords]).slice(0, 30);
            renderWords();
            hiddenInput.value = "";
            hiddenInput.focus();
        }

        function renderWords() {
            wordDisplay.innerHTML = "";
            words.forEach((word, wIdx) => {
                const wordSpan = document.createElement('span');
                wordSpan.classList.add('word');
                if (wIdx === wordIndex) wordSpan.style.borderBottom = "2px solid #e2b714";

                for (let cIdx = 0; cIdx < word.length; cIdx++) {
                    const letterSpan = document.createElement('span');
                    letterSpan.classList.add('letter');
                    letterSpan.innerText = word[cIdx];
                    wordSpan.appendChild(letterSpan);
                }
                wordDisplay.appendChild(wordSpan);
            });
        }

        function setDuration(sec) {
            duration = sec;
            document.querySelectorAll('.time-modes button').forEach(b => b.classList.remove('active'));
            document.getElementById(`btn-${sec}`).classList.add('active');
            startGame();
        }

        hiddenInput.addEventListener('input', (e) => {
            if (!isPlaying && timeLeft > 0) {
                isPlaying = true;
                timerInterval = setInterval(() => {
                    timeLeft--;
                    timerDisplay.innerText = timeLeft;
                    updateStats();
                    if (timeLeft <= 0) {
                        clearInterval(timerInterval);
                        isPlaying = false;
                        hiddenInput.blur();
                    }
                }, 1000);
            }

            if (!isPlaying) return;

            const inputVal = hiddenInput.value;
            const currentWord = words[wordIndex];
            const wordElements = wordDisplay.children[wordIndex].children;

            totalTypedChars++;

            // Boşluk tuşuna basıldıysa sonraki kelimeye geç
            if (inputVal.endsWith(' ')) {
                hiddenInput.value = "";
                wordIndex++;
                charIndex = 0;
                if (wordIndex >= words.length) {
                    words = shuffle([...osymWords]).slice(0, 20);
                    wordIndex = 0;
                }
                renderWords();
                return;
            }

            charIndex = inputVal.length;

            for (let i = 0; i < currentWord.length; i++) {
                if (i < charIndex) {
                    if (inputVal[i] === currentWord[i]) {
                        wordElements[i].classList.add('correct');
                        wordElements[i].classList.remove('incorrect');
                        correctChars++;
                    } else {
                        wordElements[i].classList.add('incorrect');
                        wordElements[i].classList.remove('correct');
                    }
                } else {
                    wordElements[i].classList.remove('correct', 'incorrect');
                }
            }
            updateStats();
        });

        function updateStats() {
            const timeElapsed = duration - timeLeft;
            if (timeElapsed > 0) {
                const wpm = Math.round((correctChars / 5) / (timeElapsed / 60));
                wpmDisplay.innerText = wpm > 0 ? wpm : 0;
            }
            if (totalTypedChars > 0) {
                const acc = Math.round((correctChars / totalTypedChars) * 100);
                accuracyDisplay.innerText = `${acc}%`;
            }
        }

        // Oyunu ilk açılışta başlat
        startGame();
    </script>
</body>
</html>
