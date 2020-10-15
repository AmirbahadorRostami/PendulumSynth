s.boot;

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
SynthDef(\vosc, {
	arg out = 0, buf = 0, numBufs = 2, freq = 300, amp = 0.0 , gate = 0;
	var sig, bufpos, detuneSig , env;

	env = EnvGen.kr(Env.asr,gate);

	detuneSig = LFNoise0.kr(0.2!8).bipolar(0.2).midiratio; //couresFX

	bufpos = buf + LFNoise1.kr(0.5).range(0,numBufs-1);
	sig = VOsc.ar(bufpos,freq * detuneSig);

	sig = Splay.ar(sig);
	sig = LeakDC.ar(sig) * amp * env;

	Out.ar(out,sig);
}).add;
)

x = Synth(\vosc,[\freq,28.midicps,\buf, ~buf[0].bufnum, \numBufs,4]);

x.set(\freq,100)
x.set(\amp ,0.5)
x.set(\gate, 1)
x.set(\gate, 0)
x.free;

//when running in RPI change to Local Address
(
NetAddr(\localhost.asString, 5005);
OSCdef('SSUListener',{
	arg msg;
	var oldFreq,oldAmp;

	if(oldFreq != msg[1],
		x.set(\freq, msg[1].midicps);
	);

	if(oldAmp != msg[2],
		x.set(\amp, msg[2]);
	);

	oldFreq = msg[1];
	oldAmp = msg[2]
},'/SC_Control');
)

(
  n = NetAddr(\localhost.asString, 5005);
  o = OSCFunc({|msg, time, from, port| msg.postln}, '/SC_Control', nil, 5005);
)