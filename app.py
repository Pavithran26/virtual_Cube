import streamlit as st
import streamlit.components.v1 as components
import cv2

import json

st.set_page_config(page_title="virtual_Cube", page_icon="🧊", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
.stApp{background:radial-gradient(ellipse at top,#172746,#080c16 65%);color:#eef4ff;font-family:'Space Grotesk',sans-serif}
header,footer{visibility:hidden}.block-container{padding-top:1.2rem;max-width:1500px}
</style>
""",unsafe_allow_html=True)
st.markdown("## 🧊 virtual_Cube · <span style='font-size:13px;color:#9db1d2'>REAL-TIME HAND TRACKING LAB</span>",unsafe_allow_html=True)
st.caption("Open palm = rotate the whole cube · Select a face, then pinch and drag to turn it.")
with st.sidebar:
 st.subheader("How to use")
 st.markdown("- Allow webcam access\n- Open palm + move: orbit cube\n- Select U / D / L / R / F / B\n- Pinch thumb + index, then move sideways: turn selected face")
 st.info("Camera frames are processed in your browser. Video is not uploaded or recorded by this app.")
 st.caption("Stack: Streamlit · OpenCV · MediaPipe Hands · Three.js")
# Firebase sign-in is hosted on Firebase Hosting, outside Streamlit's sandboxed iframe.
# This cube is a client-side demo with no protected user data or backend API.
# If [firebase_admin] is configured, verify the ID token server-side as an extra layer.
auth_component = components.declare_component(
    "virtual_cube_firebase_auth",
    url="https://virtualcube-571b7.web.app",
)
firebase_id_token = auth_component(key="firebase_auth")

if not isinstance(firebase_id_token, str) or not firebase_id_token:
    st.stop()

verified_user = None
try:
    admin_secret = st.secrets.get("firebase_admin")
except Exception:
    admin_secret = None
if admin_secret:
    try:
        import firebase_admin
        from firebase_admin import auth as firebase_admin_auth, credentials

        if not firebase_admin._apps:
            service_account_info = (
                json.loads(admin_secret["service_account_json"])
                if "service_account_json" in admin_secret
                else dict(admin_secret)
            )
            firebase_admin.initialize_app(credentials.Certificate(service_account_info))
        verified_user = firebase_admin_auth.verify_id_token(firebase_id_token, check_revoked=True)
    except Exception as exc:
        st.error(
            f"Firebase server-side token verification failed ({type(exc).__name__}). "
            "Check that the service-account key belongs to project virtualcube-571b7. "
            f"Details: {exc}"
        )
        st.stop()

if verified_user:
    st.success("Verified Google sign-in: " + verified_user.get("email", "Google user"))
else:
    st.info("Google sign-in is active. Use **Sign out** in the Firebase sign-in panel above. "
            "This demo has no protected backend data; server-side token verification is not configured.")

html = r"""\n<style>\n#auth-gate{min-height:420px;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at 50% 15%,#1b2d4b,#080e1b 70%);border:1px solid #2b3b56;border-radius:18px;color:#eef4ff;font-family:system-ui,sans-serif;padding:28px}\n.auth-card{width:min(440px,100%);padding:30px;background:#111c30;border:1px solid #354966;border-radius:20px;text-align:center;box-shadow:0 20px 70px #0005}.auth-mark{font-size:40px}.auth-card h2{margin:12px 0 5px;letter-spacing:-.04em}.auth-card p{color:#a8bbd8;font-size:13px;line-height:1.5}.auth-google{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;padding:12px 15px;border-radius:10px;border:1px solid #52637d;background:#f7f9fc;color:#1a2537;font-weight:700;cursor:pointer}.auth-google:disabled{opacity:.6;cursor:wait}.auth-google img{width:19px;height:19px}.auth-note{font-size:11px!important;color:#8198bd!important;margin-top:14px}.auth-error{color:#ffb5b5!important}.auth-user{display:none;align-items:center;gap:10px;justify-content:center;margin:12px 0 18px;font-size:12px;color:#b7c8e1}.auth-user img{width:32px;height:32px;border-radius:50%}#auth-signout{display:none;margin:0 auto 16px;border:1px solid #3a4e6c;background:#19263c;color:#dce8fa;border-radius:8px;padding:8px 12px;cursor:pointer}#vc{display:none}\n</style>\n<div id="auth-gate"><div class="auth-card"><div class="auth-mark">🧊</div><h2>Welcome to virtual_Cube</h2><p>Sign in with Google to unlock your hand-controlled Rubik’s Cube workspace.</p><div class="auth-user" id="auth-user"><img id="auth-photo" alt="" src=""><span id="auth-name"></span></div><button class="auth-google" id="auth-google"><img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="">Continue with Google</button><button id="auth-signout">Sign out</button><p id="auth-message" class="auth-note">Secure sign-in powered by Firebase Authentication.</p></div></div>\n
<div id="vc">
 <div class="bar"><span id="status">Starting scene…</span><div id="faces"><button data-f="U" class="on">U ↑</button><button data-f="D">D ↓</button><button data-f="L">L ←</button><button data-f="R">R →</button><button data-f="F">F ●</button><button data-f="B">B ◌</button></div><button id="scramble">Scramble</button><button id="reset">Reset</button></div>
 <div class="stage"><div id="scene"></div><div class="hud"><small>GESTURE</small><b id="gesture">Waiting for hand</b><small>SELECTED FACE</small><b id="selected">U · Up</b></div>
 <div class="cam"><video id="video" autoplay playsinline muted></video><canvas id="overlay"></canvas><label>● LIVE CAMERA</label></div>
 <div class="guide" id="guide"><small>INTERACTIVE TUTORIAL · <span id="num">1 / 3</span></small><h3 id="title">Meet your cube</h3><p id="body">Allow camera access and hold one hand in view with your palm facing the camera.</p><div class="arrow" id="arrow">✦</div><div class="guidebtn"><button id="prev" disabled>← Back</button><button id="next">Next step →</button><button id="hide">Hide</button></div></div></div>
 <div class="foot"><div><b>01 · ROTATE</b><span>Open palm, move your hand to orbit.</span></div><div><b>02 · SELECT</b><span>Choose the face you want to turn.</span></div><div><b>03 · TURN</b><span>Pinch and drag sideways.</span></div></div><div id="note">Camera requires permission and localhost or HTTPS. Face buttons work without a camera.</div>
</div>
<style>
#vc{background:#0a1020;border:1px solid #2b3b56;border-radius:18px;overflow:hidden;color:#edf4ff;font-family:system-ui,sans-serif}#vc *{box-sizing:border-box}
#vc button{border:1px solid #344764;background:#17243b;color:#e1ebfb;border-radius:8px;padding:8px 11px;font-weight:650;font-size:12px;cursor:pointer}#vc button:hover{border-color:#a7f3d0}#vc button.on,#vc #next{background:#a7f3d0;color:#09241d;border-color:#a7f3d0}
.bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:12px;background:#101a2d;border-bottom:1px solid #293a55;font-size:12px}.bar>span{color:#a8bddc;min-width:140px}#faces{display:flex;gap:5px;flex:1;justify-content:center}
.stage{height:530px;position:relative;background:radial-gradient(ellipse at 50% 48%,#1a2b49,#0a1223 65%);overflow:hidden}#scene{position:absolute;inset:0}#scene canvas{width:100%;height:100%;display:block}
.hud{position:absolute;top:16px;left:16px;z-index:2;background:#0b1425d9;border:1px solid #344966;border-radius:11px;padding:12px;display:flex;flex-direction:column;gap:5px;min-width:125px}.hud small,.guide small{font:10px monospace;letter-spacing:.12em;color:#86a1ca}.hud b{font-size:13px;margin-bottom:8px}.hud b:last-child{color:#a7f3d0}
.cam{position:absolute;right:14px;top:14px;width:165px;height:125px;background:#101a2c;border:1px solid #344966;border-radius:11px;overflow:hidden;z-index:3}.cam video,.cam canvas{position:absolute;width:100%;height:100%;object-fit:cover;transform:scaleX(-1)}.cam label{position:absolute;bottom:0;background:#07101ddd;padding:4px 6px;width:100%;font:9px monospace;color:#a7f3d0}
.guide{position:absolute;z-index:4;bottom:15px;left:15px;width:min(330px,calc(100% - 30px));padding:16px 17px 12px;background:#111d32f2;border:1px solid #405879;border-radius:14px;box-shadow:0 12px 40px #0006}.guide h3{font-size:19px;margin:8px 0 5px;letter-spacing:-.04em}.guide p{font-size:12px;line-height:1.5;color:#b1c1da;min-height:38px;margin:0}.arrow{position:absolute;right:18px;top:20px;font-size:24px;color:#a7f3d0}.guidebtn{display:flex;gap:6px;margin-top:13px;flex-wrap:wrap}.guidebtn button{font-size:10px!important;padding:7px 9px!important}
.foot{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#293a55}.foot div{padding:14px;background:#101a2d;display:flex;flex-direction:column;gap:6px}.foot b{font:10px monospace;letter-spacing:.1em;color:#a7f3d0}.foot span{font-size:11px;color:#afc0da;line-height:1.4}#note{padding:9px 13px;background:#0b1424;color:#8da5c8;font-size:11px;border-top:1px solid #293a55}
@media(max-width:650px){.stage{height:570px}#faces{order:3;flex-basis:100%;justify-content:flex-start}.cam{width:120px;height:90px}.foot{grid-template-columns:1fr}.foot div{padding:9px 13px}}
</style>
<script src="https://www.gstatic.com/firebasejs/10.12.5/firebase-app-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.12.5/firebase-auth-compat.js"></script><script>window.__FIREBASE_CONFIG__ = __FIREBASE_CONFIG_JSON__;</script><script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script><script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script><script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
<script>
(()=>{const $=id=>document.getElementById(id);let scene,camera,renderer,group,cubies=[],face='U',last=null,webcamController=null;
const colors={R:0xd94141,L:0xff8c38,U:0xf5f7fb,D:0xf4d83d,F:0x39bd83,B:0x3478ef},names={U:'Up',D:'Down',L:'Left',R:'Right',F:'Front',B:'Back'},mats={};
const mat=c=>mats[c]||(mats[c]=new THREE.MeshStandardMaterial({color:c,roughness:.4}));
function build(){if(group)scene.remove(group);group=new THREE.Group();cubies=[];for(let x=-1;x<=1;x++)for(let y=-1;y<=1;y++)for(let z=-1;z<=1;z++){let g=new THREE.Group();g.position.set(x*1.03,y*1.03,z*1.03);g.userData={x,y,z};g.add(new THREE.Mesh(new THREE.BoxGeometry(.96,.96,.96),mat(0x101827)));const sticker=(pos,rot,col)=>{let s=new THREE.Mesh(new THREE.PlaneGeometry(.78,.78),mat(col));s.position.copy(pos);s.rotation.set(...rot);g.add(s)};if(x===1)sticker(new THREE.Vector3(.486,0,0),[0,Math.PI/2,0],colors.R);if(x===-1)sticker(new THREE.Vector3(-.486,0,0),[0,-Math.PI/2,0],colors.L);if(y===1)sticker(new THREE.Vector3(0,.486,0),[-Math.PI/2,0,0],colors.U);if(y===-1)sticker(new THREE.Vector3(0,-.486,0),[Math.PI/2,0,0],colors.D);if(z===1)sticker(new THREE.Vector3(0,0,.486),[0,0,0],colors.F);if(z===-1)sticker(new THREE.Vector3(0,0,-.486),[0,Math.PI,0],colors.B);group.add(g);cubies.push(g)}scene.add(group)}
function init(){scene=new THREE.Scene();scene.background=new THREE.Color(0x0b1324);camera=new THREE.PerspectiveCamera(38,1,.1,100);camera.position.set(5.7,5,7.5);camera.lookAt(0,0,0);renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=THREE.SRGBColorSpace;$('scene').appendChild(renderer.domElement);scene.add(new THREE.HemisphereLight(0xdce9ff,0x34415b,2));let l=new THREE.DirectionalLight(0xffffff,2.5);l.position.set(4,7,8);scene.add(l);build();resize();window.addEventListener('resize',resize);(function draw(){requestAnimationFrame(draw);renderer.render(scene,camera)})();$('status').textContent='3D scene ready'}
function resize(){if(!renderer)return;let w=$('scene').clientWidth,h=$('scene').clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h)}
function turn(f,dir=1){let axis=['U','D'].includes(f)?'y':['L','R'].includes(f)?'x':'z',sign=['D','L','B'].includes(f)?-1:1;let pivot=new THREE.Group();scene.add(pivot);let layer=cubies.filter(c=>Math.round(c.position[axis]/1.03)===sign);layer.forEach(c=>pivot.attach(c));let start=performance.now(),angle=dir*Math.PI/2;function tick(now){let t=Math.min(1,(now-start)/220);pivot.rotation[axis]=angle*(t*t*(3-2*t));if(t<1)requestAnimationFrame(tick);else{pivot.updateMatrixWorld(true);layer.forEach(c=>{scene.attach(c);['x','y','z'].forEach(k=>{c.position[k]=Math.round(c.position[k]/1.03)*1.03;c.rotation[k]=Math.round(c.rotation[k]/(Math.PI/2))*(Math.PI/2)})});scene.remove(pivot)}}requestAnimationFrame(tick)}
function choose(f){face=f;document.querySelectorAll('#faces button').forEach(b=>b.classList.toggle('on',b.dataset.f===f));$('selected').textContent=f+' · '+names[f]}
document.querySelectorAll('#faces button').forEach(b=>b.onclick=()=>choose(b.dataset.f));$('reset').onclick=()=>{camera.position.set(5.7,5,7.5);camera.lookAt(0,0,0);build();$('note').textContent='Cube restored to solved state.'};$('scramble').onclick=()=>{let n=0,fs=Object.keys(colors);function go(){turn(fs[Math.floor(Math.random()*6)],Math.random()>.5?1:-1);if(++n<12)setTimeout(go,260)}go()};
const steps=[['Meet your cube','Allow camera access and hold one hand in view with your palm facing the camera.','✦'],['Orbit the whole cube','Spread your fingers into an open palm. Move your hand left/right or up/down to rotate the view.','↔'],['Turn one face','Select U, D, L, R, F, or B. Pinch thumb and index, then move sideways to turn that layer.','↻']];let si=0;function show(){let s=steps[si];$('num').textContent=(si+1)+' / 3';$('title').textContent=s[0];$('body').textContent=s[1];$('arrow').textContent=s[2];$('prev').disabled=si===0;$('next').textContent=si===2?'Got it ✓':'Next step →'}$('next').onclick=()=>{if(si<2){si++;show()}else $('guide').style.display='none'};$('prev').onclick=()=>{if(si){si--;show()}};$('hide').onclick=()=>$('guide').style.display='none';show();
function results(r){let can=$('overlay'),ctx=can.getContext('2d');if(can.width!==can.clientWidth*2||can.height!==can.clientHeight*2){can.width=can.clientWidth*2;can.height=can.clientHeight*2}ctx.clearRect(0,0,can.width,can.height);let h=r.multiHandLandmarks&&r.multiHandLandmarks[0];if(!h){$('gesture').textContent='Waiting for hand';last=null;return}let p=h.map(v=>({x:v.x*can.width,y:v.y*can.height}));ctx.strokeStyle='#a7f3d0';ctx.lineWidth=3;[[0,1,2,3,4],[0,5,6,7,8],[0,9,10,11,12],[0,13,14,15,16],[0,17,18,19,20]].forEach(a=>{ctx.beginPath();a.forEach((i,j)=>j?ctx.lineTo(p[i].x,p[i].y):ctx.moveTo(p[i].x,p[i].y));ctx.stroke()});p.forEach((v,i)=>{ctx.beginPath();ctx.fillStyle='#e7f0ff';ctx.arc(v.x,v.y,i===4||i===8?5:3,0,7);ctx.fill()});let pinch=Math.hypot(p[4].x-p[8].x,p[4].y-p[8].y)<can.width*.085,open=!pinch&&[8,12,16,20].every(i=>p[i].y<p[0].y+can.height*.12),c={x:(p[0].x+p[9].x)/2,y:(p[0].y+p[9].y)/2};if(pinch){$('gesture').textContent='PINCH · '+face+' FACE';if(last&&last.mode==='pinch'&&Math.abs(c.x-last.x)>can.width*.075){turn(face,c.x<last.x?1:-1);last={...c,mode:'pinch'}}else if(!last||last.mode!=='pinch')last={...c,mode:'pinch'}}else if(open){$('gesture').textContent='OPEN PALM · ROTATE';if(last&&last.mode==='open'){group.rotation.y+=(c.x-last.x)/can.width*5;group.rotation.x+=(c.y-last.y)/can.height*4}last={...c,mode:'open'}}else{$('gesture').textContent='HAND DETECTED';last=null}}
async function cameraStart(){try{let hands=new Hands({locateFile:f=>'https://cdn.jsdelivr.net/npm/@mediapipe/hands/'+f});hands.setOptions({maxNumHands:1,modelComplexity:1,minDetectionConfidence:.65,minTrackingConfidence:.55});hands.onResults(results);webcamController=new Camera($('video'),{onFrame:async()=>hands.send({image:$('video')}),width:640,height:480});await webcamController.start();$('status').textContent='Camera + hand tracking ready';$('note').textContent='Camera live. Hand landmarks are processed in your browser; video is not uploaded.'}catch(e){$('status').textContent='3D ready · camera unavailable';$('note').textContent='Camera error: '+e.message+'. Allow camera access and use localhost or HTTPS. Face buttons still work.'}}
window.startVirtualCubeCamera=cameraStart;window.stopVirtualCubeCamera=()=>{if(webcamController)webcamController.stop();const v=$('video');if(v.srcObject){v.srcObject.getTracks().forEach(t=>t.stop());v.srcObject=null;}};window.addEventListener('virtual-cube-authenticated',()=>{cameraStart();window.dispatchEvent(new Event('resize'));});try{init()}catch(e){$('status').textContent='3D initialization failed: '+e.message}
})();
</script>

<script>
(function(){
 const gate=document.getElementById('auth-gate'), app=document.getElementById('vc');
 const button=document.getElementById('auth-google'), msg=document.getElementById('auth-message');
 const signout=document.getElementById('auth-signout'), userBox=document.getElementById('auth-user');
 function showError(text){msg.textContent=text;msg.className='auth-note auth-error';}
 const cfg=window.__FIREBASE_CONFIG__;
 if(!cfg){button.disabled=true;showError('Firebase is not configured yet. Add the web app settings to Streamlit secrets, then reload.');return;}
 try{
  firebase.initializeApp(cfg); const auth=firebase.auth(); auth.setPersistence(firebase.auth.Auth.Persistence.LOCAL).catch(()=>{});
  button.addEventListener('click',async()=>{
   button.disabled=true;msg.textContent='Opening Google sign-in…';msg.className='auth-note';
   try{const provider=new firebase.auth.GoogleAuthProvider();await auth.signInWithPopup(provider);}
   catch(e){showError((e.code||'auth/error')+': '+(e.message||'Sign-in failed'));button.disabled=false;}
  });
  signout.addEventListener('click',()=>auth.signOut());
  auth.onAuthStateChanged(user=>{
   if(user){
    gate.style.display='none';app.style.display='block';window.dispatchEvent(new Event('resize'));window.dispatchEvent(new Event('virtual-cube-authenticated'));
    userBox.style.display='flex';document.getElementById('auth-name').textContent=user.displayName||user.email||'Signed in';
    const photo=document.getElementById('auth-photo');if(user.photoURL){photo.src=user.photoURL;photo.style.display='block';}else photo.style.display='none';
    button.style.display='none';signout.style.display='inline-block';
   }else{
    app.style.display='none';if(window.stopVirtualCubeCamera)window.stopVirtualCubeCamera();gate.style.display='flex';userBox.style.display='none';button.style.display='flex';button.disabled=false;signout.style.display='none';
    msg.textContent='Secure sign-in powered by Firebase Authentication.';msg.className='auth-note';
   }
  });
 }catch(e){button.disabled=true;showError('Firebase initialization failed: '+e.message);}
})();
</script>

"""
# The old embedded HTML used an iframe-based Firebase sign-in gate. Authentication now
# happens in the hosted component above. Strip the obsolete gate and keep the cube UI only.
html = html.replace("\\n", "\n")
style_start = html.find("<style>")
style_end = html.find("</style>", style_start)
if style_start >= 0 and style_end >= 0 and "#auth-gate" in html[style_start:style_end]:
    html = html[:style_start] + html[style_end + len("</style>"):]
gate_start = html.find('<div id="auth-gate">')
cube_start = html.find('<div id="vc">')
if gate_start >= 0 and cube_start >= 0 and gate_start < cube_start:
    html = html[:gate_start] + html[cube_start:]
html = html.replace(
    '<script src="https://www.gstatic.com/firebasejs/10.12.5/firebase-app-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.12.5/firebase-auth-compat.js"></script><script>window.__FIREBASE_CONFIG__ = __FIREBASE_CONFIG_JSON__;</script>',
    "",
)
# Remove the old Firebase auth listener at the end of the HTML.
auth_listener = "\n<script>\n(function(){\n const gate=document.getElementById('auth-gate')"
listener_start = html.find(auth_listener)
if listener_start >= 0:
    html = html[:listener_start]
html = html.replace('<div id="vc">', '<div id="vc" style="display:block">')
html = html.replace(
    "window.addEventListener('virtual-cube-authenticated',()=>{cameraStart();window.dispatchEvent(new Event('resize'));});",
    "cameraStart();window.dispatchEvent(new Event('resize'));",
)
components.html(html, height=760, scrolling=False)
st.caption("Local run: streamlit run app.py · Camera requires localhost or HTTPS.")
_ = cv2.__version__
