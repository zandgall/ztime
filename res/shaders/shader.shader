#shader vertex
#version 330 core

layout (location = 0) in vec3 aPos;

out vec3 pos;
out vec2 uv;

uniform mat4 screenspace, transform;

void main() {
	gl_Position = screenspace * transform * vec4(aPos, 1);
	pos = aPos;
	uv = pos.xy * 0.5 + 0.5;
}

#shader fragment
#version 330 core

in vec3 pos;
in vec2 uv;

uniform vec4 col;
uniform sampler2D tex;
uniform bool useTex;
out vec4 glColor;
void main() {
	if(useTex)
		glColor = col * texture2D(tex, uv);
	else
		glColor = col;
}