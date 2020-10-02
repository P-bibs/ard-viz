
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6

#define NUM_PIXELS 150
#define NUM_BARS 10
#define BAR_LENGTH 15

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

typedef enum {
  RED = 0,
  BLUE = 1,
  GREEN = 2
} TWEEN_COLOR ;

TWEEN_COLOR tween_from = RED;
TWEEN_COLOR tween_to = BLUE;
short progress = 0;

char serial_input_buffer[NUM_BARS];

// the setup function runs once when you press reset or power the board
void setup() {
  strip.begin();
  strip.setBrightness(255);
  
  strip.show(); // Initialize all pixels to 'off'
  
  Serial.begin(9600);
}

/*
 * brightness - number from 0 to 255 specifying pixel brightness
 */
uint32_t tweenedColor(int brightness) {

  int i;
  
  if (progress >= 100) {
    progress = 0;
    tween_from = (tween_from + 1) % 3;
    tween_to = (tween_to + 1) % 3;
  }

  int color[] = {0, 0, 0};
  color[tween_from] = (255 * (100 - progress)) / 100;
  color[tween_to] = (255 * (progress)) / 100;

  int max_color = max(max(color[0], color[1]), color[2]);
  int scale_factor = 255 / max_color;
  int brightness_factor = brightness / 255.0;

  for (i = 0; i < 3; i++) { 
    // Scale colors up to 255        
    color[i] *= scale_factor;
    // Scale colors down to 255
    color[i] *= brightness_factor;
    // Make sure colors are within range
    color[i] = min(color[i], 255);
  }

  return strip.Color(color[0], color[1], color[2]);
  
 
}

void read_to_serial_input_buffer() {
  for(int i = 0; i < NUM_BARS; i++) {
    serial_input_buffer[i] = Serial.read();
  }
}

void display_visualizer() {
  int segment_index;
  int color;
  for (int i = 0; i < NUM_BARS; i++) {
    segment_index = i * BAR_LENGTH;
    
    if (i % 2 == 0 && false) {
      color = strip.Color(serial_input_buffer[i], 0, 0);
    } else {
      color = strip.Color(0, serial_input_buffer[i], serial_input_buffer[i]);
    }
    strip.fill(color, segment_index, BAR_LENGTH);
    //strip.fill(color, i * 3, 3);
    
    //Serial.write(serial_input_buffer[i]);
  }
  //Serial.write('}');
  strip.show();
}

// the loop function runs over and over again forever
void loop() {
  if (Serial.available() >= NUM_BARS) {
    read_to_serial_input_buffer();
    display_visualizer();
//  strip.fill(strip.Color(0, serial_input_buffer[0], serial_input_buffer[0]));
//  strip.show();
    Serial.write(Serial.available());
    
    //strip.fill(tweenedColor(brightness));
    //strip.fill(strip.Color(0, brightness, 0));
    //strip.show();
    //Serial.write(brightness); // Stands for continue
  }
}
