s.boot;

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





(
~wt = Array.fill(4,{
	var numSegs = rrand(4,20);
	Env(
		[0]++
		(({rrand(0.0,1.0)}!(numSegs-1)) * [1,-1]).scramble
		++[0],
		{exprand(1,20)}!numSegs,
		{rrand(-20,20)}!numSegs
	).asSignal(1024).asWavetable;
});
)

(
~buf = Buffer.allocConsecutive(4,s,2048);
~buf.do({
	arg buf, i;
	buf.loadCollection(~wt[i]);
});
)


(
SynthDef.new(\vosc, {
	arg out = 0, buf = 0, numBufs = 2, freq = 300, amp = 0.2;
	var sig, bufpos, detuneSig;

	detuneSig = LFNoise0.kr(0.2!8).bipolar(0.2).midiratio; //couresFX

	bufpos = buf + LFNoise1.kr(0.5).range(0,numBufs-1);
	sig = VOsc.ar(bufpos,freq * detuneSig);

	sig = Splay.ar(sig);
	sig = LeakDC.ar(sig) * amp;

	Out.ar(out,sig);
}).add;
)


//when running in RPI change to Local Address
(
NetAddr(\localhost.asString, 5005);
OSCdef('SSUListener',{
	arg msg;
	Synth('fm',[freq: msg[1].midicps]);
},'/z_Rot');
)

(
NetAddr(\localhost.asString, 5005);
OSCdef('SSUListener',{
	arg msg;
	Synth('\vosc',[freq: msg[1].midicps]);
},'/z_Rot');
)

(
  n = NetAddr(\localhost.asString, 5005);
  o = OSCFunc({|msg, time, from, port| msg.postln}, '/z_Rot', nil, 5005);
)