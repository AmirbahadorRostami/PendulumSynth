( SynthDef('funsynth', {
	arg pitch = 200;
	var sound = SinOsc.ar(pitch,mul:0.2);
	var linen = Env.linen(0.01,sustainTime:0,releaseTime:1);
	var env = EnvGen.kr(linen,doneAction:2);
	Out.ar(0,sound*env);
}).add;
)

   //fm synth
	SynthDef(\fm, {
		arg freq=500, mRatio=1, cRatio=1,
		index=1, iScale=5, cAtk=4, cRel=(-4),
		amp=0.2, atk=0.01, rel=3, pan=0,
		out=0, fx=0, fxsend=(-25);
		var car, mod, env, iEnv;

		//index of modulation
		iEnv = EnvGen.kr(
			Env(
				[index, index*iScale, index],
				[atk, rel],
				[cAtk, cRel]
			)
		);

		//amplitude envelope
		env = EnvGen.kr(Env.perc(atk,rel,curve:[cAtk,cRel]),doneAction:2);

		//modulator/carrier
		mod = SinOsc.ar(freq * mRatio, mul:freq * mRatio * iEnv);
		car = SinOsc.ar(freq * cRatio + mod) * env * amp;
		car = Pan2.ar(car, pan);

		//direct out/reverb send
		Out.ar(out, car);
		Out.ar(fx, car * fxsend.dbamp);
	}).add;


//when running in RPI change to Local Address
(
NetAddr(\localhost.asString, 5005);
OSCdef('SSUListener',{
	arg msg;
	Synth('fm',[freq: msg[1].postln]);
},'/z_Rot');
)

(
  n = NetAddr(\localhost.asString, 5005);
  o = OSCFunc({|msg, time, from, port| msg.postln}, '/z_Rot', nil, 5005);
)