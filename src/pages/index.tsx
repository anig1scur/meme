import "./index.css";
import { useEffect, useRef } from "react";

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/dist/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

function Box() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let ctx = gsap.context(() => {
      ScrollTrigger.create({
        // markers: true,
        pinSpacing: false,
        invalidateOnRefresh: true,
        immediateRender: false,
        toggleActions: "restart none none reverse",
        trigger: ref.current,
        pin: "[data-action='pin']",
        start: "top center",
        end: "bottom center",
        scrub: true,
        animation: gsap.to("[data-action='disappear']", {
          scale: 0.3,
          opacity: 0,
          yPercent: 50,
        }),
      });
    }, ref);
    return () => ctx.revert();
  }, [ref]);

  return (
    <div
      data-scroll="top bottom center center"
      data-bg-img="https://tse4-mm.cn.bing.net/th/id/OIP-C.Fh5UaCuHggAYjI3yOkhwyAHaHE?w=209&h=201&c=7&r=0&o=5&dpr=1.3&pid=1.7"
      data-bg-color="#574f7d"
      className="align-items-center relative flex min-h-screen w-screen flex-col justify-center text-center text-8xl"
      ref={ref}
    >
      <div data-action="pin" className="h-64">
        I'm pinned
      </div>
      <div className="h-screen">
        <div data-action="disappear" className="h-96">
          I will disappear
        </div>
        <div>I will go </div>
      </div>
    </div>
  );
}

export default function Index() {
  const app = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let ctx = gsap.context(() => {
      const boxes = gsap.utils.toArray("[data-scroll]") as HTMLDivElement[];
      boxes.forEach((box) => {
        const tColor = box.getAttribute("data-text-color");

        const updateBg = () =>
          gsap
            .timeline()
            .to(".page", {
              color: tColor || "#fff",
            })
            .to(".page-bg-color", {
              backgroundColor: box.getAttribute("data-bg-color") || "",
              duration: 0.2,
            })
            .to(".page-bg-img", {
              opacity: 0,
              duration: 0.2,
            })
            .set(
              ".page-bg-img",
              {
                backgroundImage: `url(${box.getAttribute("data-bg-img")})`,
                backgroundPosition: `top ${gsap.utils.random(
                  0,
                  100,
                  1,
                )}% left ${gsap.utils.random(0, 100, 1)}%`,
              },
              ">",
            )
            .to(".page-bg-img", {
              opacity: 1,
              duration: 0.2,
            });

        const startEnd = box.getAttribute("data-scroll")?.split(" ");
        if (startEnd && startEnd.length === 4) {
          ScrollTrigger.create({
            trigger: box,
            start: `${startEnd[0] || "top"} ${startEnd[2] || "center"}`,
            // markers: true,
            end: `${startEnd[1] || "bottom"} ${startEnd[3] || "center"}`,
            onEnter: updateBg,
            onEnterBack: updateBg,
            immediateRender: false,
            invalidateOnRefresh: true,
          });
        }
      });
    }, app);

    return () => ctx.revert();
  }, []);

  return (
    <div className="page" ref={app}>
      <div className="page-bg sticky">
        <div className="page-bg-color fixed h-screen w-screen" />
        <div className="page-bg-img fixed h-screen w-screen bg-[length:200px_200px] bg-no-repeat" />
      </div>
      <div className="page-content">
        <div
          data-scroll="top bottom center center"
          data-bg-img="https://i.imgur.com/KJqbepD_d.webp?maxwidth=520&shape=thumb&fidelity=high"
          data-bg-color="#5F6F52"
          className="f box1"
        >
          我
        </div>
        <div
          data-scroll="top bottom center center"
          data-bg-img="https://i.pinimg.com/236x/c5/c2/c9/c5c2c916313dc5b58cfdff3635c1134d.jpg"
          data-bg-color="#A9B388"
          className="f box2"
        >
          爱
        </div>
        <div
          data-scroll="top bottom center center"
          data-bg-img="https://i.imgflip.com/87r5tz.jpg"
          data-bg-color="#B99470"
          className="f box3"
        >
          迷
        </div>
        <div
          data-scroll="top bottom center center"
          data-bg-img="https://tse2-mm.cn.bing.net/th/id/OIP-C.95Q22yqJ7r04Oqrcdvd3TAHaEJ?w=297&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
          data-bg-color="#FEFAE0"
          data-text-color="#665"
          className="f box4"
        >
          因
        </div>
      </div>
    </div>
  );
}
