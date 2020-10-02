
/*
 * progress - number from 0 to 100 specifying progress through tween
 * brightness - number from 0 to 255 specifying pixel brightness
 */
let RED = 0;
let BLUE = 1;
let GREEN = 2;
let tween_from = RED;
let tween_to = BLUE;
let progress = 0;

function tweenedColor(brightness) {

  let i;
  progress++;
  
  if (progress >= 100) {
    progress = 0;
    tween_from = (tween_from + 1) % 3;
    tween_to = (tween_to + 1) % 3;
  }

  let color = [0, 0, 0];
  color[tween_from] = (255 * (100 - progress)) / 100;
  color[tween_to] = (255 * (progress)) / 100;

  console.log(`colors after initial: ${color}`)

  let max_color = Math.max(Math.max(color[0], color[1]), color[2]);
  let scale_factor = 255 / max_color;
  let brightness_factor = brightness / 255.0;

  for (i = 0; i < 3; i++) { 
    // Scale colors up to 255        
    color[i] *= scale_factor;
    console.log(`colors after scale_factor: ${color}`)
    // Scale colors down to 255
    color[i] *= brightness_factor;
    console.log(`colors after brightners_factor: ${color}`)
    // Make sure colors are within range
    color[i] = Math.min(color[i], 255);
    console.log(`colors after max: ${color}`)
  }

  return `rgb(${color[0]}, ${color[1]}, ${color[2]})`

}

function main() {
    let t = 0;

    setInterval(() => {
        console.group();
        t++;
        console.log(t);
        let color = tweenedColor(Math.abs(Math.sin(t / 100)) * 255)
        document.body.style.backgroundColor = color;
        console.groupEnd()
    }, 10);
    
}