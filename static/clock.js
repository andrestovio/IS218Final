function drawClock() {
    const canvas = document.getElementById("clock");
    const ctx = canvas.getContext("2d");
    const radius = canvas.height / 2;
    ctx.translate(radius, radius);

    function drawFace(ctx, radius) {
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, 2 * Math.PI);
        ctx.fillStyle = "white";
        ctx.fill();

        ctx.strokeStyle = "#333";
        ctx.lineWidth = 4;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(0, 0, radius * 0.1, 0, 2 * Math.PI);
        ctx.fillStyle = "#333";
        ctx.fill();
    }

    function drawNumbers(ctx, radius) {
        const fontHeight = radius * 0.15;
        ctx.font = `${fontHeight}px arial`;
        ctx.textBaseline = "middle";
        ctx.textAlign = "center";

        for (let num = 1; num <= 12; num++) {
            const ang = (num * Math.PI) / 6;
            ctx.rotate(ang);
            ctx.translate(0, -radius * 0.85);
            ctx.rotate(-ang);
            ctx.fillText(num.toString(), 0, 0);
            ctx.rotate(ang);
            ctx.translate(0, radius * 0.85);
            ctx.rotate(-ang);
        }
    }

    function drawTime(ctx, radius) {
        const now = new Date();
        const hour = now.getHours();
        const minute = now.getMinutes();
        const second = now.getSeconds();

        const hourAngle = ((hour % 12) * Math.PI) / 6 + (minute * Math.PI) / 360;
        drawHand(ctx, hourAngle, radius * 0.5, radius * 0.07);

        const minuteAngle = (minute * Math.PI) / 30 + (second * Math.PI) / 1800;
        drawHand(ctx, minuteAngle, radius * 0.7, radius * 0.05);

        const secondAngle = (second * Math.PI) / 30;
        drawHand(ctx, secondAngle, radius * 0.9, radius * 0.02);
    }

    function drawHand(ctx, pos, length, width) {
        ctx.beginPath();
        ctx.lineWidth = width;
        ctx.lineCap = "round";
        ctx.moveTo(0, 0);
        ctx.rotate(pos);
        ctx.lineTo(0, -length);
        ctx.stroke();
        ctx.rotate(-pos);
    }

    setInterval(() => {
        ctx.clearRect(-radius, -radius, canvas.width, canvas.height);
        drawFace(ctx, radius);
        drawNumbers(ctx, radius);
        drawTime(ctx, radius);
    }, 1000);
}

drawClock();
