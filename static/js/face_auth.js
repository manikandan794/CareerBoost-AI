/* ============================================================
   CareerBoost AI — Face Unlock (client-side helper)
   ============================================================
   Uses face-api.js (a TensorFlow.js wrapper) entirely in the
   browser to turn a webcam frame into a 128-number "descriptor"
   describing the face. That descriptor — NOT the photo itself —
   is what gets sent to the server, where it's compared against
   the one stored at enrollment time.

   Loaded from a public CDN for convenience. For a real deployment,
   self-host face-api.js and its model weight files instead of
   depending on a third-party CDN.

   IMPORTANT LIMITATIONS (surface these to users in the UI, don't
   let this feel like a bank-grade security promise):
   - No liveness detection: a photo/video of the person could
     potentially fool it.
   - Requires camera permission and reasonable lighting.
   - This is a convenience alternative to a password, not a
     replacement for one — every account still needs a password.
   ============================================================ */

window.CareerBoostFaceAuth = (function () {
  const FACE_API_SRC = "https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js";
  const MODEL_URL = "https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js-models@master";

  let scriptLoadingPromise = null;
  let modelsLoadingPromise = null;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      if (document.querySelector(`script[src="${src}"]`)) return resolve();
      const s = document.createElement("script");
      s.src = src;
      s.onload = () => resolve();
      s.onerror = () => reject(new Error("Failed to load face-api.js from the CDN."));
      document.head.appendChild(s);
    });
  }

  function ensureReady() {
    if (!scriptLoadingPromise) scriptLoadingPromise = loadScript(FACE_API_SRC);
    if (!modelsLoadingPromise) {
      modelsLoadingPromise = scriptLoadingPromise.then(() =>
        Promise.all([
          faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
          faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
          faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
        ])
      );
    }
    return modelsLoadingPromise;
  }

  async function startCamera(videoEl) {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 320, height: 240 }, audio: false });
    videoEl.srcObject = stream;
    await videoEl.play();
    return stream;
  }

  function stopCamera(stream) {
    if (stream) stream.getTracks().forEach((t) => t.stop());
  }

  /** Returns a plain JS array of 128 numbers, or null if no face was found. */
  async function captureDescriptor(videoEl) {
    await ensureReady();
    const options = new faceapi.TinyFaceDetectorOptions({ inputSize: 224, scoreThreshold: 0.5 });
    const result = await faceapi
      .detectSingleFace(videoEl, options)
      .withFaceLandmarks()
      .withFaceDescriptor();
    if (!result) return null;
    return Array.from(result.descriptor);
  }

  return { ensureReady, startCamera, stopCamera, captureDescriptor };
})();
