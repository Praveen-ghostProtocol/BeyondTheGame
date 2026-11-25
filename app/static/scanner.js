/* Camera pixels stay on this device. No network upload, no automatic action. */
window.BTGScanner = (() => {
  let stream, frame, active = false;
  function stop() {
    active = false;
    if (frame) cancelAnimationFrame(frame);
    if (stream) stream.getTracks().forEach(t => t.stop());
    stream = null;
  }
  function parse(raw, origin = location.origin) {
    let code = String(raw).trim();
    if (/^https?:/i.test(code)) {
      const url = new URL(code);
      if (url.origin !== origin) throw new Error('This QR belongs to another site. Use the printed equipment ID.');
      code = url.hash.replace(/^#asset\//, '');
    } else code = code.replace(/^BTG:ASSET:/, '');
    if (!/^[A-Za-z0-9_-]{1,64}$/.test(code)) throw new Error('Unrecognized equipment QR. Enter the printed ID.');
    return code;
  }
  async function start(video, onFound, onError) {
    stop();
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
      onError('Camera needs HTTPS or localhost. Enter the equipment code below.'); return;
    }
    try {
      stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: {ideal: 'environment'}}, audio: false});
      video.srcObject = stream;
      await video.play();
      active = true;
      const canvas = document.createElement('canvas'), ctx = canvas.getContext('2d', {willReadFrequently: true});
      const tick = () => {
        if (!active) return;
        if (video.readyState >= 2) {
          const scale = Math.min(1, 800 / video.videoWidth);
          canvas.width = Math.round(video.videoWidth * scale); canvas.height = Math.round(video.videoHeight * scale);
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const found = window.jsQR(pixels.data, pixels.width, pixels.height, {inversionAttempts: 'attemptBoth'});
          if (found) {
            stop();
            try { onFound(parse(found.data)); } catch (err) { onError(err.message); }
            return;
          }
        }
        frame = requestAnimationFrame(tick);
      };
      frame = requestAnimationFrame(tick);
    } catch (err) {
      stop(); onError(err.name === 'NotAllowedError' ? 'Camera permission declined. Use the equipment code below.' : 'Camera unavailable. Use the equipment code below.');
    }
  }
  return {start, stop, parse};
})();
