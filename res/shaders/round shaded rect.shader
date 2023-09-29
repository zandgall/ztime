#shader vertex
#version 330 core

layout(location = 0) in vec3 aPos;

out vec3 pos;
out vec2 uv;
out vec2 transform_size;

uniform mat4 screenspace, transform;

void main() {
	gl_Position = screenspace * transform * vec4(aPos, 1);
	pos = aPos;
	uv = pos.xy * 0.5 + 0.5;
	transform_size.x = transform[0].x;
	transform_size.y = transform[1].y;
}

#shader fragment
#version 330 core

in vec3 pos;
in vec2 uv;
in vec2 transform_size;

uniform vec3 hslcol;
uniform sampler2D tex;
uniform bool useTex;
uniform float rounding;
uniform float shadingAmount;
out vec4 glColor;
float roundrect(vec2 val, vec2 size, float round) {
	//float d = length(max(abs(size*val)+round, size)) - round;
	float d = length(vec2(max(abs(size.x * val.x) + round, size.x) - size.x, max(abs(size.y * val.y) + round, size.y) - size.y)) - round;
	return max(1-d, 0);
}

float fromhue(float p, float q, float t) {
	if (t < 0) 
		t += 1;
	if (t > 1) 
		t -= 1;
  	if (t < 1.0/6.0) 
		return p + (q - p) * 6 * t;
  	if (t < 1.0/2.0) 
		return q;
  	if (t < 2.0/3.0) 
		return p + (q - p) * (2.0/3.0 - t) * 6;
	return p;
}

vec3 hsl_to_rgb(vec3 hsl) {
	float h = hsl.x;
	float s = clamp(hsl.y, 0, 1);
	float l = clamp(hsl.z, 0, 1);
	if(s == 0)
		return vec3(l);
	float q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    float p = 2.0 * l - q;
	return vec3(fromhue(p, q, h + 1.0/3.0), fromhue(p, q, h), fromhue(p, q, h - 1.0/3.0));
}

void main() {
	float alpha = roundrect(uv * 2 - 1, transform_size, rounding);
	float shade = distance(uv, vec2(1));
	vec4 color = vec4(hsl_to_rgb(hslcol + mix(vec3(0, 0*0.5-0*(shade*0.5-0.5), shade*0.5-0.5), vec3(0,0,0), clamp(alpha-3, 0, 1))*shadingAmount), 1);
	// vec4 color = vec4(hsl_to_rgb(hslcol), 1);
	// color.x = shade;
	// color.y = shade;
	// color.z = hslcol.z;
	// color.xyz = hslcol;
	if (useTex)
		glColor = color * texture2D(tex, uv);
	else
		glColor = color;
	
	// glColor.xyz *= mix(1, mix(shade+0.2, 1, clamp(alpha-3, 0, 1)), shadingAmount);
	glColor.w *= alpha;
}