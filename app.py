<!DOCTYPE html>
<html>
<head>
    <title>Emoji AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .card { border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        canvas { border: 2px solid #ddd; border-radius: 10px; cursor: crosshair; }
        .result-emoji { font-size: 4rem; }
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="card p-4 text-center">
            <h1>🎨 AI Nhận diện Emoji</h1>
            <p class="text-muted">Vẽ lên khung trắng</p>
            
            <canvas id="canvas" width="280" height="280" class="mx-auto" style="background: white;"></canvas><br>
            <button class="btn btn-danger" onclick="clearCanvas()">🗑️ Xóa</button>
            <button class="btn btn-primary" onclick="predict()">🔍 Dự đoán</button>
            
            <div id="result" class="mt-4" style="display: none;">
                <div class="alert alert-success">
                    <div class="result-emoji" id="emoji"></div>
                    <h3 id="className"></h3>
                    <p id="confidence"></p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let drawing = false;
        
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 15;
        
        canvas.addEventListener('mousedown', () => drawing = true);
        canvas.addEventListener('mouseup', () => drawing = false);
        canvas.addEventListener('mousemove', (e) => {
            if (!drawing) return;
            const rect = canvas.getBoundingClientRect();
            ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
        });
        
        function clearCanvas() {
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.beginPath();
            document.getElementById('result').style.display = 'none';
        }
        
        async function predict() {
            const dataURL = canvas.toDataURL('image/png');
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({image: dataURL})
            });
            const data = await response.json();
            
            document.getElementById('emoji').innerHTML = data.emoji;
            document.getElementById('className').innerHTML = data.class;
            document.getElementById('confidence').innerHTML = `Độ tin cậy: ${(data.confidence*100).toFixed(1)}%`;
            document.getElementById('result').style.display = 'block';
        }
    </script>
</body>
</html>
