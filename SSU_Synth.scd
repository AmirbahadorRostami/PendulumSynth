( SynthDef('funsynth', {
	arg pitch = 200;
	var sound = SinOsc.ar(pitch,mul:0.2);
	var linen = Env.linen(0.01,sustainTime:0,releaseTime:1);
	var env = EnvGen.kr(linen,doneAction:2);
	Out.ar(0,sound*env);
}).add;
)

//when running in RPI change to Local Address
(
NetAddr(\localhost.asString, 5005);
OSCdef('SSUListener',{
	arg msg;
	Synth('funsynth',[pitch: msg[1].postln]);
},'/z_Rot');
)

(
  n = NetAddr(\localhost.asString, 5005);
  o = OSCFunc({|msg, time, from, port| msg.postln}, '/z_Rot', nil, 5005);
)