s.waitForBoot{

    ("jack_connect SuperCollider:out_1 alsa_out:playback_1 &".unixCmd;
		"jack_connect SuperCollider:out_2 alsa_out:playback_2 &".unixCmd;);

    (
b= OSCresponderNode(nil,'/medium DataPacket',{arg t,r,msg; Ndef(\bass).set(\t_trig,msg[1],\freq,msg[1]);}).add
);

(
v= OSCresponderNode(nil,'/small DataPacket',{arg t,r,msg; Ndef(\snd).set(\t_trig,msg[1],\freq,msg[1]);}).add
);

(
r= OSCresponderNode(nil,'/big DataPacket',{arg t,r,msg; Ndef(\drone).set(\t_trig,msg[1],\freq,msg[1]);}).add
);

/////

(
l= OSCresponderNode(nil,'/Probe response',{arg t,r,msg; Ndef(\base).set(\t_trig,msg[1],\break2,msg[1]);}).add
);




(Ndef(\snd, { arg freq=600, decay=0.5, t_trig=1;
	var env = EnvGen.ar(Env.triangle (0.2, decay), t_trig);

		Pan2.ar(
			SinOsc.ar(freq/2,0.1)
			* LFCub.ar(freq/2,10)
		* env )
	;
}).play);





(Ndef(\drone, { arg freq=600,decay=0.5,resfreq=1,t_trig=1;

	var env = EnvGen.ar(Env.triangle (25, decay), t_trig);

	Pan2.ar(
		 RLPF.ar(
			Saw.ar([100,150,300])*(resfreq*LFNoise0.kr([3, freq/1000, 7])),
			LinLin.kr(freq,600,1200, 350, 700),
			0.05)
	)*env;

}).play);


(Ndef(\bass, { arg freq=600, decay=0.5, t_trig=1,break=1;
	var env = EnvGen.ar(Env.sine (1, decay), t_trig);
	Pan2.ar(

			RLPF.ar(
			LFPulse.ar(LinLin.kr(freq,3000,6000, 3700, 1200))
			*SinOsc.kr([break,LinLin.kr(break,3000,6000, 700, 1200),6])
			


	)*1)* env

	;
}).play);


(Ndef(\base, { arg freq=600, decay=0.9, t_trig=1,break2;
	var env = EnvGen.ar(Env.perc (0.1, decay), t_trig);

		Pan2.ar(
		 LFPulse.ar(LFPulse.kr(7, 0, 0.3, 400, 200), 0, 0.1, 0.1) 
			
		* env )
	;
}).play);




};
