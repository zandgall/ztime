#shader vertex
#version 330 core

layout (location = 0) in vec3 aPos;

out vec2 uv;

uniform mat4 screenspace, transform;

void main() {
	gl_Position = screenspace * transform * vec4(aPos, 1);
	uv = aPos.xy * 0.5 + 0.5;
}

#shader fragment
#version 330 core

in vec2 uv;
uniform sampler2D tex;

out vec4 glColor;
void main() {
    ivec2 tex_size = textureSize(tex, 0);
    vec2 one_pixel = vec2(1.0)/tex_size;
    vec2 pixel_y = vec2(0, one_pixel.y);
    vec2 pixel_x = vec2(one_pixel.x, 0);

	vec3 current = texture2D(tex, uv).xyz;

    glColor = vec4(current, 1);
    
    
    if(current==vec3(1,0,0)&&texture2D(tex, uv+pixel_y).xyz == vec3(1)) // If red, and below white, set self to white
        glColor = vec4(1);
    else if(current==vec3(1) && texture2D(tex, uv-pixel_y).xyz==vec3(1,0,0)) // If white, and above red, set self to red
        glColor = vec4(1,0,0,1);
    else if(current==vec3(1,0,0)&&texture2D(tex, uv+pixel_y).xyz==vec3(0)&&texture2D(tex, uv+pixel_x+pixel_y).xyz==vec3(1)) // If red, and below black, and below and right white, set to white
        glColor = vec4(1);
    else if(current==vec3(1) && texture2D(tex, uv-pixel_x).xyz==vec3(0)&&texture2D(tex, uv-pixel_x-pixel_y).xyz==vec3(1,0,0)) // if white, and to the left black, and left and up red, set to red
        glColor = vec4(1,0,0,1);
}