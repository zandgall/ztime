#define NBT_COMPILE
#include "App.h"
#include "../base/glhelper.h"
#include "../appwork/appwork.h"
#include "../base/networker.h"
#include "Assets.h"
#include "TimeDoc.h"

#define timestamp() (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now().time_since_epoch()).count())

const bool AABB(glm::vec4 a, glm::vec4 b) { return (a.x + a.z >= b.x && a.x <= b.x + b.z) && (a.y + a.w >= b.y && a.y <= b.y + b.w); }

void canvas_draw(app::component* component);
app::component* canvas;

App* App::instance = nullptr;

TimeDoc document = TimeDoc();

double xscale = 1.0/60.0, yscale = 60.0, yoffset = 0;
unsigned long long begin = 1695387500;

App::App() {
	loadAssets();
	
	instance = this;

	window = app::create_window("Window", SCREEN_WIDTH, SCREEN_HEIGHT);
	window->clear_color = glm::vec4(0.8, 0.9, 1, 1);

	canvas = new app::component(0, 0, window->width, window->height);
	window->addComponent(canvas);
	canvas->draw.push_back(&canvas_draw);
}

long long last = 0;
void App::tick(double delta) {
	if (glfwWindowShouldClose(window->glfw_window))
		glfwSetWindowShouldClose(WINDOW, GLFW_TRUE);
	if(window->keys[GLFW_KEY_LEFT_CONTROL])
		xscale += xscale * 0.1 * window->mouseScroll;
	else if(window->keys[GLFW_KEY_LEFT_ALT])
		yscale += yscale * 0.1 * window->mouseScroll;
	else if(window->keys[GLFW_KEY_LEFT_SHIFT])
		yoffset += window->mouseScroll;
	else
		begin -= (unsigned long long)(100/xscale * window->mouseScroll);
}

void App::render() {}

glm::vec3 toHSL(glm::vec3 rgb) {
	float r = rgb.x;
	float g = rgb.y;
	float b = rgb.z;
	float vmax = std::max(r, std::max(g, b)), vmin = std::min(r, std::min(g, b));
	if(vmax == vmin)
		return glm::vec3(0, 0, (vmax+vmin)/2.f);
	
	float h = (vmax + vmin) / 2.f;
	float s = (vmax + vmin) / 2.f;
	float l = (vmax + vmin) / 2.f;
	float d = vmax - vmin;
	s = l > 0.5 ? d / (2 - vmax - vmin) : d / (vmax + vmin);
	if(vmax == r) h = (g - b) / d + (g < b ? 6 : 0);
	if(vmax == g) h = (b - r) / d + 2;
	if(vmax == b) h = (r - g) / d + 4;
	h/=6.0;
	return glm::vec3(h, s, l);
}

void canvas_draw(app::component* canvas) {
	glUseProgram(_getGLShader("default shader"));
	uniMat("screenspace", glm::ortho<float>(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0));
	glUseProgram(_getGLShader("round shaded rect shader"));
	uniMat("screenspace", glm::ortho<float>(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0));
	uniFloat("rounding", yscale * 0.2);
	uniFloat("shadingAmount", 0.5f);
	for(auto entry: document.entries) {
		glUseProgram(_getGLShader("round shaded rect shader"));
		size_t layer = document.type_layers[entry.type];
		uniMat("transform", rect(((long long)entry.begin - (long long)begin)*xscale, layer*yscale + yoffset*yscale, (entry.end-entry.begin)*xscale, yscale));
		uniVec("hslcol", toHSL(document.types[entry.type]));
		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
		glUseProgram(_getGLShader("default shader"));
		uniVec("col", glm::vec4(0,0,0,1));
		glm::vec3 m = measureString(entry.type, "roboto");
		float scale = std::min(yscale / m.z, (entry.end-entry.begin)*xscale / m.x);
		drawString(entry.type, "roboto", scale, ((long long)entry.begin-(long long)begin)*xscale, (layer+1)*yscale + yoffset*yscale - (yscale - m.y * scale)*0.5);
	}
}