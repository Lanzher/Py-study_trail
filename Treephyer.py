import tkinter as tk
from tkinter import simpledialog, messagebox, Menu, filedialog, scrolledtext
import math
import json

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ===================== 多语言 =====================
LANGUAGES = {
    'zh': {
        'lang_name': '简体中文',
        'title': '物理蟒状图（测试体验壹） v1.29.31',
        'menu_center_rect': '创建中心矩形 (80x40)',
        'menu_edge_rect': '创建边缘矩形 (60x30)',
        'menu_custom_rect': '创建自定义矩形',
        'menu_circle': '创建圆形',
        'menu_create': '图形创建',
        'menu_delete': '删除此图形',
        'menu_resize': '自定义大小',
        'menu_nail': '创建钉子',
        'menu_nail_resize': '调整钉子大小',
        'menu_delete_nail': '删除此钉子',
        'menu_nail_line': '从此钉子拉线',
        'menu_line_type': '连线模式',
        'menu_line_straight': '直线连接',
        'menu_line_curve': '曲线连接（带控制点）',
        'menu_line_freehand': '手绘连线（自由绘制）',
        'menu_eraser': '橡皮擦',
        'menu_set_length': '设置长度（弹簧）',
        'menu_infinite': '无限（无拉力）',
        'menu_finite': '有限（输入值）',
        'menu_delete_line': '删除此线',
        'tutorial_title': '教程',
        'tutorial_text': (
            "⚠️ 已知 Bug 提醒 ⚠️\n"
            "• 钉子拖动时极小概率画出轨迹线，可生成一条新线再删除来消除。\n"
            "• 若钉子不在最上层，重新生成一个钉子可恢复默认图层。\n"
            "• 设置线条长度时如果卡住，切换回桌面再返回可恢复。\n"
            "• 文字若未显示，生成一个钉子可强制刷新图层。\n"
            "• 自由绘制线（手绘）操作可能存在错误率，建议谨慎使用。\n\n"
            "操作教程：\n\n"
            "【创建】\n"
            "• 右键空白处 → 图形创建子菜单，可创建矩形或圆形\n"
            "• 右键空白处 → 创建钉子（灰色实心圆）\n\n"
            "【移动与物理】\n"
            "• 左键拖动图形 → 举起（不受重力），松开后掉落\n"
            "• 拖动时若靠近钉子，边框变黄，松开即被钉住（变绿）\n"
            "• 钉子可拖动，钉住的图形随之移动\n"
            "• 点击图形选中（黄框），按 WASD 改变该图形重力方向\n"
            "• 选中时显示红色重力方向线（mg线）\n"
            "• 精确碰撞，堆叠紧密不悬空\n\n"
            "【旋转】\n"
            "• 选中图形后，滚动鼠标滚轮可旋转（每次15°）\n\n"
            "【紧急制动】\n"
            "• 按 空格键 让所有图形瞬间停止运动\n\n"
            "【多选】\n"
            "• 按住 Ctrl 键点击图形或钉子，可多选/取消选中\n"
            "• 多选状态下拖动，所有选中图形和钉子一起移动\n"
            "• 多选后按 Ctrl+Delete 可批量删除选中的图形（钉子需单独删除）\n\n"
            "【连线】\n"
            "• 点击图形两侧小三角 → 开始/完成连线（支持直线/曲线/手绘）\n"
            "• 画线时，鼠标靠近钉子会自动吸附，左键点击即可连接到钉子\n"
            "• 画线过程中，右键点击可取消临时线\n"
            "• 右键点击钉子 → 从此钉子拉线（起点为钉子中心）\n"
            "• 右键点击已存在的连线 → 删除或设置弹簧长度（有限/无限）\n"
            "• 线条会随钉子移动而更新\n"
            "• 手绘线：直接左键拖动即可移动（无需Ctrl），右键可删除\n\n"
            "【橡皮擦】\n"
            "• 右键菜单 → 橡皮擦，鼠标变为方块，滚轮调节大小\n"
            "• 点击手绘线可擦除一段笔迹（点击位置附近会被截断）\n"
            "• 点击普通直线/曲线则整条删除，再次点击菜单退出橡皮擦\n\n"
            "【编辑与删除】\n"
            "• 左键单击图形（不拖动）→ 输入文字\n"
            "• 右键点击图形 → 删除或自定义大小\n"
            "• 右键点击钉子 → 调整半径、删除或拉线\n\n"
            "【导出】\n"
            "• 点击左上角语言按钮 → 导出数据（JSON）或导出为图片（JPG/PNG）\n\n"
            "【性能提示】\n"
            "• 图形数量较多（>50）时物理计算可能变慢，建议保持简洁。\n"
            "• 弹簧长度约束会额外计算，可按需设置。\n\n"
            "【开源声明】\n"
            "本程序完全免费开源，欢迎学习、使用、修改。\n"
            "若您基于本程序二次开发，请保留原作者信息。\n"
            "项目地址：https://github.com/Lanzher/GraphysicalPyXP1\n"
        ),
        'resize_rect_title': '自定义矩形大小',
        'resize_rect_prompt_w': '请输入宽度（像素）：',
        'resize_rect_prompt_h': '请输入高度（像素）：',
        'resize_circle_title': '自定义圆形半径',
        'resize_circle_prompt': '请输入半径（像素）：',
        'resize_nail_title': '调整钉子大小',
        'resize_nail_prompt': '请输入新半径（像素）：',
        'input_text_title': '输入文字',
        'input_text_prompt': '请输入文字：',
        'confirm_delete_shape': '确认删除图形',
        'confirm_delete_shape_msg': '确定要删除此图形及其所有连线吗？',
        'confirm_delete_nail': '确认删除钉子',
        'confirm_delete_nail_msg': '确定要删除此钉子吗？（被钉住的图形将被释放）',
        'error_invalid_number': '请输入有效数字',
        'line_deleted': '已删除该连线',
        'lang_switch': '切换语言',
        'lang_zh': '简体中文',
        'lang_en': 'English',
        'set_length_prompt': '请输入弹簧自然长度（像素）：',
        'line_length_set': '弹簧长度已设置为 {} 像素',
        'line_length_infinite': '弹簧已设为无限（无拉力）',
        'contact_title': '联系我 / Contact Me',
        'contact_msg': (
            "物理蟒状图（测试体验壹） v1.29.31\n"
            "GraphysicalPyXP1\n\n"
            "哔哩哔哩/Bilibili：晓心许Luo_\n\n"
            "我是个Python业余爱好者，只有初高中Py的基础应试知识，还有学业。\n"
            "初代测试程序粗糙，由我和DeepSeek共同开发编写，\n"
            "有些bug本人和AI暂无法解决，愿谅解！\n\n"
            "邮箱 / Email: quseriama@qq.com\n"
            "GitHub: https://github.com/Lanzher\n"
            "欢迎您提出建议！ / Welcome your suggestions!\n\n"
            "【开源声明】\n"
            "本程序完全免费开源，欢迎学习、使用、修改。\n"
            "若您基于本程序二次开发，请保留原作者信息。"
        ),
        'nail_line_start': '已开始从钉子拉线，点击目标（图形三角或钉子）完成连线，右键取消。',
        'export_title': '导出数据',
        'export_filetypes': 'JSON 文件 (*.json)',
        'export_success': '数据已成功导出到：{}',
        'export_error': '导出失败：{}',
        'export_image_title': '导出为图片',
        'export_image_success': '图片已导出到：{}',
        'export_image_fail': '导出图片失败，请确认已安装 Pillow 库。',
        'freehand_instruction': '手绘模式：按住左键绘制，松开完成（或右键取消）',
        'eraser_on': '橡皮擦已开启（滚轮调大小，点击擦除/删除线条）',
        'eraser_off': '橡皮擦已关闭'
    },
    'en': {
        'lang_name': 'English',
        'title': 'GraphysicalPyXP1 v1.29.31',
        'menu_center_rect': 'Create Center Rect (80x40)',
        'menu_edge_rect': 'Create Edge Rect (60x30)',
        'menu_custom_rect': 'Create Custom Rect',
        'menu_circle': 'Create Circle',
        'menu_create': 'Create Shape',
        'menu_delete': 'Delete this Shape',
        'menu_resize': 'Resize Shape',
        'menu_nail': 'Create Nail',
        'menu_nail_resize': 'Resize Nail',
        'menu_delete_nail': 'Delete this Nail',
        'menu_nail_line': 'Draw line from this nail',
        'menu_line_type': 'Line Mode',
        'menu_line_straight': 'Straight Line',
        'menu_line_curve': 'Curve Line (with control point)',
        'menu_line_freehand': 'Freehand Draw',
        'menu_eraser': 'Eraser',
        'menu_set_length': 'Set Length (Spring)',
        'menu_infinite': 'Infinite (no force)',
        'menu_finite': 'Finite (enter value)',
        'menu_delete_line': 'Delete this Line',
        'tutorial_title': 'Tutorial',
        'tutorial_text': (
            "⚠️ Known Bug Alert ⚠️\n"
            "• Nail dragging may rarely draw a ghost line; draw and delete a new line to clear it.\n"
            "• If a nail is not on top, create a new nail to restore default layer order.\n"
            "• If setting line length freezes, switch to desktop and back.\n"
            "• If text not showing, create a nail to force layer refresh.\n"
            "• Freehand lines may have issues, use with caution.\n\n"
            "Tutorial:\n\n"
            "[Create]\n"
            "• Right-click on blank area → Create Shape submenu, create Rect or Circle\n"
            "• Right-click on blank area → Create Nail (gray solid circle)\n\n"
            "[Move & Physics]\n"
            "• Left drag shape → lift (no gravity), drop when released\n"
            "• Border turns yellow when near a nail, release to pin (turns green)\n"
            "• Nails can be dragged, pinned shapes move with them\n"
            "• Click shape to select (yellow border), press WASD to change gravity direction\n"
            "• Red arrow shows gravity direction (mg line) when selected\n"
            "• Precise collision with tight stacking\n\n"
            "[Rotate]\n"
            "• Select a shape and scroll mouse wheel to rotate (15° per step)\n\n"
            "[Emergency Brake]\n"
            "• Press SPACE to instantly stop all shapes\n\n"
            "[Multi-select]\n"
            "• Hold Ctrl and click shapes or nails to toggle selection\n"
            "• Drag while multi-selected to move all selected shapes and nails together\n"
            "• Press Ctrl+Delete to delete selected shapes (nails separately)\n\n"
            "[Lines]\n"
            "• Click small triangles on sides → start/complete line (straight/curve/freehand)\n"
            "• While drawing, moving near a nail will snap the line to it; click to connect\n"
            "• Right-click during drawing to cancel the temporary line\n"
            "• Right-click nail → Draw line from this nail (start at nail center)\n"
            "• Lines update when nails move\n"
            "• Freehand lines: left-click and drag to move directly\n\n"
            "[Eraser]\n"
            "• Right-click menu → Eraser, mouse becomes square, scroll to resize\n"
            "• Click on freehand line to erase a segment (near click point)\n"
            "• Click on straight/curve lines to delete entirely\n\n"
            "[Edit & Delete]\n"
            "• Left click shape (no drag) → input text\n"
            "• Right-click shape → delete or resize\n"
            "• Right-click nail → resize, delete, or draw line from it\n\n"
            "[Export]\n"
            "• Click the top-left language button → Export Data (JSON) or Export Image (JPG/PNG)\n\n"
            "[Performance Tips]\n"
            "• Too many shapes (>50) may slow down physics, keep it moderate.\n"
            "• Spring constraints add extra calculation, use only when needed.\n\n"
            "[Open Source Notice]\n"
            "This program is completely free and open source.\n"
            "Feel free to learn, use, and modify.\n"
            "If you build upon it, please retain the original author info.\n"
            "Repo: https://github.com/Lanzher/GraphysicalPyXP1\n"
        ),
        'resize_rect_title': 'Resize Rectangle',
        'resize_rect_prompt_w': 'Enter width (pixels):',
        'resize_rect_prompt_h': 'Enter height (pixels):',
        'resize_circle_title': 'Resize Circle',
        'resize_circle_prompt': 'Enter radius (pixels):',
        'resize_nail_title': 'Resize Nail',
        'resize_nail_prompt': 'Enter new radius (pixels):',
        'input_text_title': 'Input Text',
        'input_text_prompt': 'Enter text:',
        'confirm_delete_shape': 'Confirm Delete Shape',
        'confirm_delete_shape_msg': 'Are you sure to delete this shape and all its lines?',
        'confirm_delete_nail': 'Confirm Delete Nail',
        'confirm_delete_nail_msg': 'Are you sure to delete this nail? (Pinned shape will be released)',
        'error_invalid_number': 'Please enter a valid number',
        'line_deleted': 'Line deleted',
        'lang_switch': 'Switch Language',
        'lang_zh': '简体中文',
        'lang_en': 'English',
        'set_length_prompt': 'Enter spring natural length (pixels):',
        'line_length_set': 'Spring length set to {} pixels',
        'line_length_infinite': 'Spring set to infinite (no force)',
        'contact_title': 'Contact Me',
        'contact_msg': (
            "GraphysicalPyXP1 v1.29.31\n\n"
            "Bilibili: 晓心许Luo_\n\n"
            "I'm a Python hobbyist with only basic knowledge from high school.\n"
            "This prototype is developed by me and DeepSeek.\n"
            "Some bugs are not yet resolved, your understanding is appreciated!\n\n"
            "Email: quseriama@qq.com\n"
            "GitHub: https://github.com/Lanzher\n"
            "Welcome your suggestions!\n\n"
            "[Open Source Notice]\n"
            "This program is completely free and open source.\n"
            "Feel free to learn, use, and modify.\n"
            "If you build upon it, please retain the original author info."
        ),
        'nail_line_start': 'Started line from nail, click target (shape triangle or nail) to complete, right-click to cancel.',
        'export_title': 'Export Data',
        'export_filetypes': 'JSON files (*.json)',
        'export_success': 'Data exported successfully to: {}',
        'export_error': 'Export failed: {}',
        'export_image_title': 'Export Image',
        'export_image_success': 'Image exported to: {}',
        'export_image_fail': 'Export image failed. Please install Pillow library.',
        'freehand_instruction': 'Freehand: hold left button to draw, release to finish (or right-click to cancel)',
        'eraser_on': 'Eraser ON (scroll to resize, click to erase/delete)',
        'eraser_off': 'Eraser OFF'
    }
}

# ===================== 图形基类 =====================
class Shape:
    def __init__(self, canvas, x, y, fill="white", outline="black", text=""):
        self.canvas = canvas
        self.x, self.y = x, y
        self.fill = fill
        self.outline = outline
        self.text = text
        self.vx = self.vy = 0.0
        self.gx, self.gy = 0.0, 1.0
        self.gravity_magnitude = 0.2
        self.pinned_nail = None
        self.is_dragging = False
        self.angle = 0.0
        self.left_vertex = self.right_vertex = (0, 0)
        self.tri_left = self.tri_right = None
        self.rect_id = self.text_id = None
        self.selected = False
        self.mg_line = self.mg_arrow = None

    def update_position(self, nx, ny):
        dx, dy = nx - self.x, ny - self.y
        self.x, self.y = nx, ny
        for item in (self.rect_id, self.text_id, self.tri_left, self.tri_right):
            if item:
                self.canvas.move(item, dx, dy)
        self._update_vertices()
        self.update_mg_line()
        if self.text_id:
            self.canvas.tag_raise(self.text_id)

    def _update_vertices(self):
        pass

    def set_outline(self, color):
        if self.rect_id:
            self.canvas.itemconfig(self.rect_id, outline=color)

    def delete(self):
        for item in (self.rect_id, self.text_id, self.tri_left, self.tri_right):
            if item:
                self.canvas.delete(item)
        for key in (self.tri_left, self.tri_right):
            if key and key in self.canvas.tri_to_rect:
                del self.canvas.tri_to_rect[key]
        self.remove_mg_line()

    def get_anchor(self, direction):
        return self.left_vertex if direction == 'left' else self.right_vertex

    def update_mg_line(self):
        self.remove_mg_line()
        if not self.selected:
            return
        length = 50
        dx, dy = self.gx * length, self.gy * length
        x1, y1, x2, y2 = self.x, self.y, self.x + dx, self.y + dy
        self.mg_line = self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2)
        angle = math.atan2(dy, dx)
        a_len, a_ang = 10, math.pi/6
        p1 = (x2 - a_len * math.cos(angle - a_ang), y2 - a_len * math.sin(angle - a_ang))
        p2 = (x2 - a_len * math.cos(angle + a_ang), y2 - a_len * math.sin(angle + a_ang))
        self.mg_arrow = self.canvas.create_polygon(x2, y2, p1[0], p1[1], p2[0], p2[1], fill='red', outline='red')

    def remove_mg_line(self):
        if self.mg_line:
            self.canvas.delete(self.mg_line)
            self.mg_line = None
        if self.mg_arrow:
            self.canvas.delete(self.mg_arrow)
            self.mg_arrow = None

    def set_gravity_direction(self, gx, gy):
        norm = math.hypot(gx, gy)
        self.gx, self.gy = (gx/norm, gy/norm) if norm > 0 else (0, 1)
        self.update_mg_line()

    def rotate(self, delta):
        self.angle += delta
        self._update_vertices()

    def _rotate_point(self, px, py, cx, cy, ang):
        dx, dy = px - cx, py - cy
        c, s = math.cos(ang), math.sin(ang)
        return cx + dx*c - dy*s, cy + dx*s + dy*c

    @property
    def radius(self):
        if hasattr(self, 'w'):
            return max(self.w, self.h) / 2
        elif hasattr(self, 'r'):
            return self.r
        return 20

# ===================== 矩形 =====================
class RectObject(Shape):
    def __init__(self, canvas, x, y, w, h, fill="white", outline="black", text=""):
        super().__init__(canvas, x, y, fill, outline, text)
        self.w, self.h = w, h
        self.shape_type = 'rect'
        self.angle = 0.0
        self._update_vertices()
        self._create_triangles()
        canvas.tri_to_rect[self.tri_left] = (self, 'left')
        canvas.tri_to_rect[self.tri_right] = (self, 'right')

    def _create_triangles(self):
        for t in (self.tri_left, self.tri_right):
            if t:
                self.canvas.delete(t)
        lx, ly = self.left_vertex
        rx, ry = self.right_vertex
        ts = 8
        self.tri_left = self.canvas.create_polygon(
            lx, ly, lx+ts/2, ly-ts/2, lx+ts/2, ly+ts/2, fill='black', outline='black', tags=('tri',))
        self.tri_right = self.canvas.create_polygon(
            rx, ry, rx-ts/2, ry-ts/2, rx-ts/2, ry+ts/2, fill='black', outline='black', tags=('tri',))
        for t in (self.tri_left, self.tri_right):
            if t in self.canvas.tri_to_rect:
                del self.canvas.tri_to_rect[t]
        self.canvas.tri_to_rect[self.tri_left] = (self, 'left')
        self.canvas.tri_to_rect[self.tri_right] = (self, 'right')

    def _update_vertices(self):
        hw, hh = self.w/2, self.h/2
        corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        abs_verts = [(self.x + px, self.y + py) for px, py in 
                     [self._rotate_point(cx, cy, 0, 0, self.angle) for cx, cy in corners]]
        flat = [c for p in abs_verts for c in p]
        if self.rect_id is None:
            self.rect_id = self.canvas.create_polygon(flat, fill=self.fill, outline=self.outline, width=2)
        else:
            self.canvas.coords(self.rect_id, *flat)
            self.canvas.itemconfig(self.rect_id, fill=self.fill, outline=self.outline)
        lpos = self._rotate_point(-hw, 0, 0, 0, self.angle)
        rpos = self._rotate_point(hw, 0, 0, 0, self.angle)
        self.left_vertex = (self.x + lpos[0], self.y + lpos[1])
        self.right_vertex = (self.x + rpos[0], self.y + rpos[1])
        self._create_triangles()
        if self.text_id is not None:
            self.canvas.coords(self.text_id, self.x, self.y)
            self.canvas.tag_raise(self.text_id)
        else:
            self.text_id = self.canvas.create_text(self.x, self.y, text=self.text, font=("Arial", 10))
            self.canvas.tag_raise(self.text_id)

    def set_size(self, w, h):
        self.w, self.h = w, h
        self._update_vertices()

    def collision_data(self):
        return ('rect', self.x, self.y, self.w, self.h, 0)

# ===================== 圆形 =====================
class CircleObject(Shape):
    def __init__(self, canvas, x, y, r, fill="lightgreen", outline="black", text=""):
        super().__init__(canvas, x, y, fill, outline, text)
        self.r = r
        self.shape_type = 'circle'
        self.angle = 0.0
        self.rect_id = canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=2)
        self.text_id = canvas.create_text(x, y, text=text, font=("Arial", 10))
        self._update_vertices()
        canvas.tri_to_rect[self.tri_left] = (self, 'left')
        canvas.tri_to_rect[self.tri_right] = (self, 'right')
        self.canvas.tag_raise(self.text_id)

    def _update_vertices(self):
        ts = 8
        lpos = self._rotate_point(-self.r, 0, 0, 0, self.angle)
        rpos = self._rotate_point(self.r, 0, 0, 0, self.angle)
        self.left_vertex = (self.x + lpos[0], self.y + lpos[1])
        self.right_vertex = (self.x + rpos[0], self.y + rpos[1])
        for t in (self.tri_left, self.tri_right):
            if t:
                self.canvas.delete(t)
        lx, ly = self.left_vertex
        rx, ry = self.right_vertex
        self.tri_left = self.canvas.create_polygon(
            lx, ly, lx+ts/2, ly-ts/2, lx+ts/2, ly+ts/2, fill='black', outline='black', tags=('tri',))
        self.tri_right = self.canvas.create_polygon(
            rx, ry, rx-ts/2, ry-ts/2, rx-ts/2, ry+ts/2, fill='black', outline='black', tags=('tri',))
        for t in (self.tri_left, self.tri_right):
            if t in self.canvas.tri_to_rect:
                del self.canvas.tri_to_rect[t]
        self.canvas.tri_to_rect[self.tri_left] = (self, 'left')
        self.canvas.tri_to_rect[self.tri_right] = (self, 'right')
        if self.text_id is not None:
            self.canvas.coords(self.text_id, self.x, self.y)
            self.canvas.tag_raise(self.text_id)
        else:
            self.text_id = self.canvas.create_text(self.x, self.y, text=self.text, font=("Arial", 10))
            self.canvas.tag_raise(self.text_id)

    def set_radius(self, r):
        self.r = r
        self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r,
                                               fill=self.fill, outline=self.outline, width=2)
        self._update_vertices()

    def collision_data(self):
        return ('circle', self.x, self.y, 0, 0, self.r)

# ===================== 钉子 =====================
class Nail:
    def __init__(self, canvas, x, y, radius=8):
        self.canvas = canvas
        self.x, self.y = x, y
        self.radius = radius
        self.pinned_shape = None
        self.circle_id = canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                            fill="gray", outline="black", width=2)
        self.highlight = False
        self.selected = False

    def update_position(self, nx, ny):
        dx, dy = nx - self.x, ny - self.y
        self.x, self.y = nx, ny
        self.canvas.move(self.circle_id, dx, dy)
        if self.pinned_shape:
            self.pinned_shape.update_position(self.pinned_shape.x + dx, self.pinned_shape.y + dy)
            app = self.canvas.app
            if app:
                app.update_lines_for_shape(self.pinned_shape)
        app = self.canvas.app
        if app:
            app.update_lines_for_nail(self)
        self.canvas.tag_raise(self.circle_id)

    def set_radius(self, r):
        self.radius = r
        self.canvas.delete(self.circle_id)
        self.circle_id = self.canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r,
                                                 fill="gray", outline="black", width=2)
        self.canvas.tag_raise(self.circle_id)

    def set_highlight(self, on):
        self.highlight = on
        self.canvas.itemconfig(self.circle_id, outline="orange" if on else "black")

    def set_selected(self, on):
        self.selected = on
        self.canvas.itemconfig(self.circle_id, outline="yellow" if on else ("orange" if self.highlight else "black"))

    def delete(self):
        self.canvas.delete(self.circle_id)
        if self.pinned_shape:
            self.pinned_shape.pinned_nail = None
            self.pinned_shape.set_outline("black")
            self.pinned_shape = None

    def get_anchor(self, _=None):
        return (self.x, self.y)

# ===================== 主应用 =====================
class TreeApp:
    def __init__(self, root):
        self.root = root
        self.lang_code = 'zh'
        self.lang = LANGUAGES[self.lang_code]
        root.title(self.lang['title'])
        root.geometry("900x700")
        root.configure(bg='white')
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.running = True

        self.canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.app = self

        self.shapes, self.nails, self.lines = [], [], []
        self.canvas.tri_to_rect = {}
        self.start_tri = None
        self.temp_line = None
        self.line_type = 'straight'
        self.drag_shape = self.drag_nail = None
        self.drag_line_id = None
        self.drag_offset_x = self.drag_offset_y = 0
        self.drag_occurred = False
        self.update_interval = 80
        self.after_id = None
        self.selected_objects = []
        self.freehand_data = {}

        # 物理参数
        self.gravity_magnitude = 0.2
        self.spring_stiffness = 0.02
        self.spring_damping = 0.97
        self.ground_friction = 0.98
        self.bounce_damping = 0.6
        self.static_friction_threshold = 0.15
        self.ground_y = 650

        # 橡皮擦
        self.eraser_mode = False
        self.eraser_size = 8
        self.eraser_square = None
        self.eraser_radius = 6

        # 语言按钮
        self.lang_btn = tk.Label(root, text="中", bg="lightgray", relief="solid", borderwidth=1,
                                 font=("Arial", 10, "bold"), width=4, height=2)
        self.lang_btn.place(x=10, y=10, anchor='nw')
        self.lang_btn.bind("<Button-1>", self.show_menu)

        # 右键菜单
        self.context_menu = Menu(root, tearoff=0)
        self.create_menu = Menu(self.context_menu, tearoff=0)
        self.create_menu.add_command(label=self.lang['menu_center_rect'], command=self.create_center_rect)
        self.create_menu.add_command(label=self.lang['menu_edge_rect'], command=self.create_outer_rect)
        self.create_menu.add_command(label=self.lang['menu_custom_rect'], command=self.create_custom_rect)
        self.create_menu.add_command(label=self.lang['menu_circle'], command=self.create_circle)
        self.context_menu.add_cascade(label=self.lang['menu_create'], menu=self.create_menu)

        self.context_menu.add_command(label=self.lang['menu_nail'], command=self.create_nail)
        self.context_menu.add_command(label=self.lang['menu_nail_resize'], command=self.resize_nail)
        self.context_menu.add_command(label=self.lang['menu_delete_nail'], command=self.delete_selected_nail)
        self.context_menu.add_command(label=self.lang['menu_nail_line'], command=self.start_line_from_nail)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.lang['menu_delete'], command=self.delete_selected_shape)
        self.context_menu.add_command(label=self.lang['menu_resize'], command=self.resize_selected_shape)
        self.context_menu.add_separator()
        self.line_menu = Menu(self.context_menu, tearoff=0)
        self.line_menu.add_command(label=self.lang['menu_line_straight'], command=lambda: self.set_line_type('straight'))
        self.line_menu.add_command(label=self.lang['menu_line_curve'], command=lambda: self.set_line_type('curve'))
        self.line_menu.add_command(label=self.lang['menu_line_freehand'], command=lambda: self.set_line_type('freehand'))
        self.context_menu.add_cascade(label=self.lang['menu_line_type'], menu=self.line_menu)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.lang['menu_eraser'], command=self.toggle_eraser)

        self.right_click_shape = self.right_click_nail = None
        self.context_click_pos = (0, 0)

        # 地面线
        self.ground_line = self.canvas.create_line(0, self.ground_y, self.canvas.winfo_width(), self.ground_y,
                                                   fill="brown", width=3)

        # 键盘绑定
        root.bind("<Key>", self.on_key_press)
        root.bind("<Button-3>", self.on_right_click_canvas)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)
        self.canvas.bind("<Button-5>", self.on_mousewheel)

        self.canvas.bind("<Button-1>", self.on_left_down)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_up)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # 手绘状态
        self.freehand_points = []
        self.freehand_line = None
        self.is_freehand_drawing = False

        self.update_physics()

    def on_closing(self):
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.root.destroy()

    # ===================== 菜单 =====================
    def show_menu(self, event):
        menu = Menu(self.root, tearoff=0)
        menu.add_command(label="简体中文", command=lambda: self.set_language('zh'))
        menu.add_command(label="English", command=lambda: self.set_language('en'))
        menu.add_separator()
        menu.add_command(label=self.lang['tutorial_title'], command=self.show_tutorial)
        menu.add_separator()
        menu.add_command(label="导出数据 / Export Data", command=self.export_data)
        menu.add_command(label="导出为图片 / Export Image", command=self.export_image)
        menu.add_separator()
        menu.add_command(label="联系我 / Contact Me", command=self.show_contact)
        menu.post(event.x_root, event.y_root)

    def set_language(self, code):
        self.lang_code = code
        self.lang = LANGUAGES[code]
        self.root.title(self.lang['title'])
        self.lang_btn.config(text="中" if code == 'zh' else "En")
        # 更新菜单项
        self.create_menu.entryconfig(0, label=self.lang['menu_center_rect'])
        self.create_menu.entryconfig(1, label=self.lang['menu_edge_rect'])
        self.create_menu.entryconfig(2, label=self.lang['menu_custom_rect'])
        self.create_menu.entryconfig(3, label=self.lang['menu_circle'])
        self.context_menu.entryconfig(0, label=self.lang['menu_create'])
        self.context_menu.entryconfig(1, label=self.lang['menu_nail'])
        self.context_menu.entryconfig(2, label=self.lang['menu_nail_resize'])
        self.context_menu.entryconfig(3, label=self.lang['menu_delete_nail'])
        self.context_menu.entryconfig(4, label=self.lang['menu_nail_line'])
        self.context_menu.entryconfig(6, label=self.lang['menu_delete'])
        self.context_menu.entryconfig(7, label=self.lang['menu_resize'])
        self.line_menu.entryconfig(0, label=self.lang['menu_line_straight'])
        self.line_menu.entryconfig(1, label=self.lang['menu_line_curve'])
        self.line_menu.entryconfig(2, label=self.lang['menu_line_freehand'])
        self.context_menu.entryconfig(9, label=self.lang['menu_line_type'])
        self.context_menu.entryconfig(11, label=self.lang['menu_eraser'])

    def show_tutorial(self):
        win = tk.Toplevel(self.root)
        win.title(self.lang['tutorial_title'])
        win.geometry("600x500")
        text = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Arial", 10))
        content = self.lang['tutorial_text']
        content += "\n\n【个人说明】\n我是个Python业余爱好者，只有初高中Py的基础应试知识，还有学业。\n初代测试程序粗糙，由我和DeepSeek共同开发编写，\n有些bug本人和AI暂无法解决，愿谅解！\n\n【B站】晓心许Luo_\n【开源声明】本程序完全免费开源，欢迎学习、使用、修改。\n若您基于本程序二次开发，请保留原作者信息。"
        text.insert("1.0", content)
        text.config(state=tk.NORMAL)
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        tk.Label(win, text="（可选中文字后用 Ctrl+C 复制）", font=("Arial", 8), fg="gray").pack(pady=(0,5))

    def show_contact(self):
        win = tk.Toplevel(self.root)
        win.title(self.lang['contact_title'])
        win.geometry("500x300")
        win.resizable(False, False)
        text = tk.Text(win, wrap=tk.WORD, font=("Arial", 10))
        text.insert("1.0", self.lang['contact_msg'])
        text.config(state=tk.NORMAL)
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        tk.Label(win, text="（可选中文字后用 Ctrl+C 复制）", font=("Arial", 8), fg="gray").pack(pady=(0,5))

    # ===================== 导出 =====================
    def export_data(self):
        data = {"shapes": [], "nails": [], "lines": []}
        for s in self.shapes:
            info = {"type": s.shape_type, "x": s.x, "y": s.y, "text": s.text,
                    "angle": s.angle, "fill": s.fill, "outline": s.outline}
            if hasattr(s, 'w'):
                info.update({"w": s.w, "h": s.h})
            elif hasattr(s, 'r'):
                info["r"] = s.r
            data["shapes"].append(info)
        for n in self.nails:
            data["nails"].append({"x": n.x, "y": n.y, "radius": n.radius})
        for lid, start_obj, start_dir, end_obj, end_dir, lt, cid, sl in self.lines:
            def get_idx(obj):
                if isinstance(obj, Shape):
                    try: return self.shapes.index(obj)
                    except: return None
                elif isinstance(obj, Nail):
                    try: return -self.nails.index(obj) - 1
                    except: return None
            si, ei = get_idx(start_obj), get_idx(end_obj)
            if si is not None and ei is not None:
                data["lines"].append({"start_idx": si, "start_dir": start_dir,
                                      "end_idx": ei, "end_dir": end_dir,
                                      "line_type": lt, "spring_length": sl})
        path = filedialog.asksaveasfilename(title=self.lang['export_title'],
                                            defaultextension=".json",
                                            filetypes=[(self.lang['export_filetypes'], "*.json")])
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("", self.lang['export_success'].format(path))
            except Exception as e:
                messagebox.showerror("", self.lang['export_error'].format(str(e)))

    def export_image(self):
        if not HAS_PIL:
            messagebox.showerror("", self.lang['export_image_fail'])
            return
        path = filedialog.asksaveasfilename(title=self.lang['export_image_title'],
                                            defaultextension=".jpg",
                                            filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")])
        if path:
            try:
                ps = self.canvas.postscript(colormode='color')
                from io import BytesIO
                img = Image.open(BytesIO(ps.encode('utf-8')))
                if path.lower().endswith('.jpg') or path.lower().endswith('.jpeg'):
                    img = img.convert('RGB')
                    img.save(path, 'JPEG', quality=90)
                else:
                    img.save(path)
                messagebox.showinfo("", self.lang['export_image_success'].format(path))
            except Exception as e:
                messagebox.showerror("", str(e))

    # ===================== 物理引擎 =====================
    def update_physics(self):
        if not self.running:
            return
        canvas_w = self.canvas.winfo_width()
        for s in self.shapes:
            if s.pinned_nail is None and not s.is_dragging:
                s.vx += s.gx * self.gravity_magnitude
                s.vy += s.gy * self.gravity_magnitude
                nx, ny = s.x + s.vx, s.y + s.vy
                r = s.radius
                if nx - r < 0:
                    nx, s.vx = r, -s.vx * self.bounce_damping
                elif nx + r > canvas_w:
                    nx, s.vx = canvas_w - r, -s.vx * self.bounce_damping
                if ny - r < 0:
                    ny, s.vy = r, -s.vy * self.bounce_damping
                elif ny + r > self.ground_y:
                    ny, s.vy = self.ground_y - r, -s.vy * self.bounce_damping
                    s.vx *= self.ground_friction
                if nx != s.x or ny != s.y:
                    s.update_position(nx, ny)
                    self.update_lines_for_shape(s)

        # 弹簧力
        for lid, start_obj, start_dir, end_obj, end_dir, lt, cid, sl in self.lines:
            if sl is not None:
                x1, y1 = start_obj.get_anchor(start_dir) if isinstance(start_obj, Shape) else start_obj.get_anchor()
                x2, y2 = end_obj.get_anchor(end_dir) if isinstance(end_obj, Shape) else end_obj.get_anchor()
                dx, dy = x2 - x1, y2 - y1
                dist = math.hypot(dx, dy)
                if dist > 1e-6:
                    force = (dist - sl) * self.spring_stiffness
                    nx, ny = dx / dist, dy / dist
                    for obj in (start_obj, end_obj):
                        if isinstance(obj, Shape) and obj.pinned_nail is None and not obj.is_dragging:
                            obj.vx += nx * (force if obj is start_obj else -force)
                            obj.vy += ny * (force if obj is start_obj else -force)
                            obj.vx *= self.spring_damping
                            obj.vy *= self.spring_damping

        # 碰撞
        for i in range(len(self.shapes)):
            for j in range(i+1, len(self.shapes)):
                self.resolve_collision(self.shapes[i], self.shapes[j])

        self.after_id = self.root.after(self.update_interval, self.update_physics)

    def resolve_collision(self, a, b):
        def get_data(obj):
            if isinstance(obj, RectObject):
                return ('rect', obj.x, obj.y, obj.w, obj.h, 0)
            else:
                return ('circle', obj.x, obj.y, 0, 0, obj.r)

        ta, xa, ya, wa, ha, ra = get_data(a)
        tb, xb, yb, wb, hb, rb = get_data(b)

        if ta == 'rect' and tb == 'rect':
            hw_a, hh_a = wa/2, ha/2
            hw_b, hh_b = wb/2, hb/2
            dx, dy = xb - xa, yb - ya
            ox = hw_a + hw_b - abs(dx)
            oy = hh_a + hh_b - abs(dy)
            if ox > 0 and oy > 0:
                if ox < oy:
                    nx, ny = (1 if dx>0 else -1), 0
                    overlap = ox
                else:
                    nx, ny = 0, (1 if dy>0 else -1)
                    overlap = oy
                self._apply_push(a, b, nx, ny, overlap)

        elif ta == 'circle' and tb == 'circle':
            dx, dy = xb - xa, yb - ya
            dist = math.hypot(dx, dy)
            min_dist = ra + rb
            if dist < min_dist and dist > 1e-6:
                nx, ny = dx/dist, dy/dist
                overlap = min_dist - dist
                self._apply_push(a, b, nx, ny, overlap)
                self._snap_to_contact(a, b, nx, ny, min_dist)

        else:
            r_a = max(wa, ha)/2 if ta == 'rect' else ra
            r_b = rb if tb == 'circle' else max(wb, hb)/2
            dx, dy = xb - xa, yb - ya
            dist = math.hypot(dx, dy)
            min_dist = r_a + r_b
            if dist < min_dist and dist > 1e-6:
                nx, ny = dx/dist, dy/dist
                overlap = min_dist - dist
                self._apply_push(a, b, nx, ny, overlap)
                self._snap_to_contact(a, b, nx, ny, min_dist)

    def _apply_push(self, a, b, nx, ny, overlap):
        ma = (a.w * a.h) if hasattr(a, 'w') else (a.r * a.r)
        mb = (b.w * b.h) if hasattr(b, 'w') else (b.r * b.r)
        total = ma + mb
        if total == 0: total = 1
        push_a = overlap * (mb / total) * 0.5
        push_b = overlap * (ma / total) * 0.5
        if a.pinned_nail is None and not a.is_dragging:
            a.update_position(a.x - nx * push_a, a.y - ny * push_a)
            self.update_lines_for_shape(a)
        if b.pinned_nail is None and not b.is_dragging:
            b.update_position(b.x + nx * push_b, b.y + ny * push_b)
            self.update_lines_for_shape(b)
        rel_v = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny
        if abs(rel_v) < self.static_friction_threshold:
            if a.pinned_nail is None and not a.is_dragging:
                a.vx -= (a.vx - b.vx) * 0.5
                a.vy -= (a.vy - b.vy) * 0.5
            if b.pinned_nail is None and not b.is_dragging:
                b.vx += (a.vx - b.vx) * 0.5
                b.vy += (a.vy - b.vy) * 0.5
        elif rel_v > 0:
            impulse = rel_v * (1 + 0.3)
            if a.pinned_nail is None and not a.is_dragging:
                a.vx -= impulse * nx * (mb / total)
                a.vy -= impulse * ny * (mb / total)
                a.vx *= self.bounce_damping
                a.vy *= self.bounce_damping
            if b.pinned_nail is None and not b.is_dragging:
                b.vx += impulse * nx * (ma / total)
                b.vy += impulse * ny * (ma / total)
                b.vx *= self.bounce_damping
                b.vy *= self.bounce_damping

    def _snap_to_contact(self, a, b, nx, ny, target_dist):
        dx = b.x - a.x
        dy = b.y - a.y
        dist = math.hypot(dx, dy)
        if dist > 1e-6:
            diff = dist - target_dist
            ma = (a.w * a.h) if hasattr(a, 'w') else (a.r * a.r)
            mb = (b.w * b.h) if hasattr(b, 'w') else (b.r * b.r)
            total = ma + mb
            if total == 0: total = 1
            if a.pinned_nail is None and not a.is_dragging:
                a.x -= dx / dist * diff * (mb / total) * 0.5
                a.y -= dy / dist * diff * (mb / total) * 0.5
                a.update_position(a.x, a.y)
                self.update_lines_for_shape(a)
            if b.pinned_nail is None and not b.is_dragging:
                b.x += dx / dist * diff * (ma / total) * 0.5
                b.y += dy / dist * diff * (ma / total) * 0.5
                b.update_position(b.x, b.y)
                self.update_lines_for_shape(b)

    # ===================== 线条更新 =====================
    def update_lines_for_shape(self, shape):
        for line in self.lines:
            lid, start_obj, start_dir, end_obj, end_dir, lt, cid, sl = line
            if (isinstance(start_obj, Shape) and start_obj is shape) or (isinstance(end_obj, Shape) and end_obj is shape):
                self._update_line(lid, start_obj, start_dir, end_obj, end_dir, lt, cid)

    def update_lines_for_nail(self, nail):
        for line in self.lines:
            lid, start_obj, start_dir, end_obj, end_dir, lt, cid, sl = line
            if start_obj is nail or end_obj is nail:
                self._update_line(lid, start_obj, start_dir, end_obj, end_dir, lt, cid)

    def _update_line(self, lid, start_obj, start_dir, end_obj, end_dir, lt, cid):
        x1, y1 = start_obj.get_anchor(start_dir) if isinstance(start_obj, Shape) else start_obj.get_anchor()
        x2, y2 = end_obj.get_anchor(end_dir) if isinstance(end_obj, Shape) else end_obj.get_anchor()
        if lt == 'straight':
            self.canvas.coords(lid, x1, y1, x2, y2)
            if cid:
                self.canvas.delete(cid)
                for i, (lid2, *_) in enumerate(self.lines):
                    if lid2 == lid:
                        self.lines[i] = (lid2, start_obj, start_dir, end_obj, end_dir, lt, None, sl)
                        break
        elif lt == 'curve':
            if cid:
                coords = self.canvas.coords(cid)
                if coords:
                    cx, cy = (coords[0]+coords[2])/2, (coords[1]+coords[3])/2
                else:
                    cx, cy = (x1+x2)/2, (y1+y2)/2 - 30
                self.canvas.coords(lid, x1, y1, cx, cy, x2, y2)
            else:
                cx, cy = (x1+x2)/2, (y1+y2)/2 - 30
                self.canvas.coords(lid, x1, y1, cx, cy, x2, y2)
        # 手绘线不更新

    # ===================== 连线模式 =====================
    def set_line_type(self, mode):
        self.line_type = mode
        if mode == 'freehand':
            messagebox.showinfo("", self.lang['freehand_instruction'])

    def handle_tri_click(self, tri_id):
        shape, direction = self.canvas.tri_to_rect[tri_id]
        if self.line_type == 'freehand':
            self.start_freehand(shape, direction)
        else:
            self._start_or_finish_line(shape, direction)

    def start_freehand(self, obj, direction):
        self.freehand_points = []
        self.is_freehand_drawing = True
        self.start_tri = (obj, direction)
        x0, y0 = obj.get_anchor(direction) if isinstance(obj, Shape) else obj.get_anchor()
        self.freehand_points.append((x0, y0))
        self.temp_line = self.canvas.create_line(x0, y0, x0, y0, fill='black', width=2)
        self.canvas.bind("<B1-Motion>", self.on_freehand_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_freehand_release)
        self.canvas.bind("<Button-3>", self.on_freehand_cancel)

    def on_freehand_drag(self, event):
        if not self.is_freehand_drawing:
            return
        x, y = event.x, event.y
        self.freehand_points.append((x, y))
        if len(self.freehand_points) >= 2:
            if self.temp_line:
                self.canvas.delete(self.temp_line)
            pts = [coord for point in self.freehand_points for coord in point]
            self.temp_line = self.canvas.create_line(pts, fill='black', width=2, smooth=True)

    def on_freehand_release(self, event):
        if not self.is_freehand_drawing:
            return
        self.is_freehand_drawing = False
        if len(self.freehand_points) >= 3:
            pts = [coord for point in self.freehand_points for coord in point]
            lid = self.canvas.create_line(pts, fill='black', width=2, smooth=True)
            self.lines.append((lid, None, None, None, None, 'freehand', None, None))
            self.freehand_data[lid] = self.freehand_points[:]
        else:
            self.canvas.delete(self.temp_line)
        self.temp_line = None
        self.start_tri = None
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Button-3>")
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_up)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.refresh_layers()

    def on_freehand_cancel(self, event):
        if self.is_freehand_drawing:
            self.canvas.delete(self.temp_line)
            self.temp_line = None
            self.is_freehand_drawing = False
            self.start_tri = None
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.unbind("<Button-3>")
            self.canvas.bind("<B1-Motion>", self.on_left_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_left_up)
            self.canvas.bind("<Button-3>", self.on_right_click)

    def _start_or_finish_line(self, obj, direction):
        cur = (obj, direction)
        if self.start_tri is None:
            self.start_tri = cur
            x0, y0 = obj.get_anchor(direction) if isinstance(obj, Shape) else obj.get_anchor()
            self.temp_line = self.canvas.create_line(x0, y0, x0, y0, fill='black', width=2, dash=(4,2))
        else:
            if self.start_tri == cur:
                self.cancel_temp_line()
            else:
                start_obj, start_dir = self.start_tri
                end_obj, end_dir = cur
                x1, y1 = start_obj.get_anchor(start_dir) if isinstance(start_obj, Shape) else start_obj.get_anchor()
                x2, y2 = end_obj.get_anchor(end_dir) if isinstance(end_obj, Shape) else end_obj.get_anchor()
                if self.line_type == 'straight':
                    lid = self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
                    cid = None
                else:
                    cx, cy = (x1+x2)/2, (y1+y2)/2 - 30
                    lid = self.canvas.create_line(x1, y1, cx, cy, x2, y2, fill='black', width=2, smooth=True)
                    cid = self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill='red', outline='red')
                    self.canvas.tag_bind(cid, "<B1-Motion>", lambda e, lid=lid, cid=cid: self.on_control_drag(e, lid, cid))
                self.lines.append((lid, start_obj, start_dir, end_obj, end_dir, self.line_type, cid, None))
                self.canvas.tag_bind(lid, "<Button-3>", lambda e, lid=lid: self.on_line_right_click(e, lid))
                self.canvas.delete(self.temp_line)
                self.temp_line = None
                self.start_tri = None
                self.refresh_layers()

    def cancel_temp_line(self):
        if self.temp_line:
            self.canvas.delete(self.temp_line)
            self.temp_line = None
        self.start_tri = None
        for n in self.nails:
            n.set_highlight(False)

    # ---- 控制点拖动（曲线） ----
    def on_control_drag(self, event, lid, cid):
        cx, cy = event.x, event.y
        self.canvas.coords(cid, cx-5, cy-5, cx+5, cy+5)
        for lid2, s1, d1, s2, d2, lt, cid2, sl in self.lines:
            if lid2 == lid:
                x1, y1 = s1.get_anchor(d1) if isinstance(s1, Shape) else s1.get_anchor()
                x2, y2 = s2.get_anchor(d2) if isinstance(s2, Shape) else s2.get_anchor()
                self.canvas.coords(lid, x1, y1, cx, cy, x2, y2)
                break

    def on_line_right_click(self, event, lid):
        menu = Menu(self.root, tearoff=0)
        menu.add_command(label=self.lang['menu_delete_line'], command=lambda: self.delete_line(lid))
        for lid2, s1, d1, s2, d2, lt, cid, sl in self.lines:
            if lid2 == lid and lt != 'freehand':
                length_menu = Menu(menu, tearoff=0)
                length_menu.add_command(label=self.lang['menu_infinite'], command=lambda: self.set_line_length(lid, None))
                length_menu.add_command(label=self.lang['menu_finite'], command=lambda: self.set_line_length(lid, 'finite'))
                menu.add_cascade(label=self.lang['menu_set_length'], menu=length_menu)
                break
        menu.post(event.x_root, event.y_root)

    def set_line_length(self, lid, mode):
        for idx, (lid2, s1, d1, s2, d2, lt, cid, old) in enumerate(self.lines):
            if lid2 == lid:
                if mode is None:
                    new_len = None
                    messagebox.showinfo("", self.lang['line_length_infinite'])
                else:
                    win = tk.Toplevel(self.root)
                    win.title(self.lang['menu_set_length'])
                    win.geometry("300x120")
                    win.resizable(False, False)
                    tk.Label(win, text=self.lang['set_length_prompt']).pack(pady=5)
                    entry = tk.Entry(win)
                    entry.pack(pady=5)
                    entry.focus_set()
                    result = None
                    def ok():
                        nonlocal result
                        try:
                            val = float(entry.get())
                            if val >= 1.0:
                                result = val
                            else:
                                messagebox.showerror("", self.lang['error_invalid_number'])
                                return
                        except:
                            messagebox.showerror("", self.lang['error_invalid_number'])
                            return
                        win.destroy()
                    def cancel():
                        win.destroy()
                    tk.Button(win, text="确定", command=ok).pack(side=tk.LEFT, padx=20, pady=10)
                    tk.Button(win, text="取消", command=cancel).pack(side=tk.RIGHT, padx=20, pady=10)
                    self.root.wait_window(win)
                    if result is not None:
                        new_len = result
                        messagebox.showinfo("", self.lang['line_length_set'].format(new_len))
                    else:
                        return
                self.lines[idx] = (lid2, s1, d1, s2, d2, lt, cid, new_len)
                break

    def delete_line(self, lid):
        for idx, (lid2, s1, d1, s2, d2, lt, cid, sl) in enumerate(self.lines):
            if lid2 == lid:
                self.canvas.delete(lid2)
                if cid:
                    self.canvas.delete(cid)
                if lid in self.freehand_data:
                    del self.freehand_data[lid]
                del self.lines[idx]
                break

    # ---- 部分擦除手绘线 ----
    def erase_segment(self, lid, x, y):
        if lid not in self.freehand_data:
            return
        points = self.freehand_data[lid]
        # 找最近点
        min_dist = float('inf')
        idx = -1
        for i, (px, py) in enumerate(points):
            d = math.hypot(px - x, py - y)
            if d < min_dist:
                min_dist = d
                idx = i
        if idx == -1:
            return
        erase_radius = max(8, self.eraser_size * 1.5)
        keep_indices = []
        for i, (px, py) in enumerate(points):
            if math.hypot(px - points[idx][0], py - points[idx][1]) > erase_radius:
                keep_indices.append(i)
        if len(keep_indices) < 3:
            self.delete_line(lid)
            return
        new_points = [points[i] for i in keep_indices]
        self.freehand_data[lid] = new_points
        flat = [coord for p in new_points for coord in p]
        self.canvas.coords(lid, *flat)
        self.canvas.update_idletasks()

    # ===================== 橡皮擦 =====================
    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.root.config(cursor="none")
            self.eraser_size = 8
            self.update_eraser_square(0, 0)
            messagebox.showinfo("", self.lang['eraser_on'])
        else:
            self.root.config(cursor="")
            if self.eraser_square:
                self.canvas.delete(self.eraser_square)
                self.eraser_square = None
            messagebox.showinfo("", self.lang['eraser_off'])

    def update_eraser_square(self, x, y):
        if self.eraser_square:
            self.canvas.delete(self.eraser_square)
        half = self.eraser_size // 2
        self.eraser_square = self.canvas.create_rectangle(
            x - half, y - half, x + half, y + half,
            fill='black', outline='white', width=1
        )

    # ===================== 鼠标和键盘事件 =====================
    def on_mouse_move(self, event):
        if self.eraser_mode:
            self.update_eraser_square(event.x, event.y)
        else:
            if self.start_tri and self.temp_line and self.line_type != 'freehand':
                x, y = event.x, event.y
                start_obj, start_dir = self.start_tri
                x0, y0 = start_obj.get_anchor(start_dir) if isinstance(start_obj, Shape) else start_obj.get_anchor()
                snapped = False
                for n in self.nails:
                    if math.hypot(x - n.x, y - n.y) <= n.radius + 15:
                        x, y = n.x, n.y
                        n.set_highlight(True)
                        snapped = True
                        break
                if not snapped:
                    for n in self.nails:
                        n.set_highlight(False)
                self.canvas.coords(self.temp_line, x0, y0, x, y)

    def on_key_press(self, e):
        if e.keysym == 'Delete' and (e.state & 0x0004):
            for s in self.selected_objects[:]:
                if isinstance(s, Shape):
                    self.delete_shape(s)
                elif isinstance(s, Nail):
                    self.delete_nail(s)
                elif isinstance(s, int):
                    self.delete_line(s)
            self.selected_objects = []
            return
        if e.keysym == 'space':
            for s in self.shapes:
                s.vx = s.vy = 0.0
            return
        if not self.selected_objects:
            return
        key = e.keysym.lower()
        for obj in self.selected_objects:
            if isinstance(obj, Shape):
                if key == 'w':
                    obj.set_gravity_direction(0, -1)
                elif key == 's':
                    obj.set_gravity_direction(0, 1)
                elif key == 'a':
                    obj.set_gravity_direction(-1, 0)
                elif key == 'd':
                    obj.set_gravity_direction(1, 0)

    def on_mousewheel(self, e):
        if self.eraser_mode:
            delta = 2 if (e.num == 4 or e.delta > 0) else -2
            self.eraser_size = max(4, self.eraser_size + delta)
            x, y = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(), self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
            self.update_eraser_square(x, y)
            return
        shapes = [obj for obj in self.selected_objects if isinstance(obj, Shape)]
        if not shapes:
            return
        delta = math.radians(15 if (e.num == 4 or e.delta > 0) else -15)
        for s in shapes:
            s.rotate(delta)
            self.update_lines_for_shape(s)

    # ===================== 左键拖动 =====================
    def on_left_down(self, e):
        self.drag_occurred = False
        x, y = e.x, e.y

        # 橡皮擦模式：点击擦除
        if self.eraser_mode:
            items = self.canvas.find_overlapping(x-2, y-2, x+2, y+2)
            for item in items:
                for lid, *rest in self.lines:
                    if item == lid and lid in self.freehand_data:
                        self.erase_segment(lid, x, y)
                        return
                for lid, *rest in self.lines:
                    if item == lid:
                        self.delete_line(lid)
                        return
            return

        if self.start_tri and self.line_type != 'freehand':
            for n in self.nails:
                if math.hypot(x - n.x, y - n.y) <= n.radius + 5:
                    self.finish_line_to_nail(n)
                    return
            for item in self.canvas.find_overlapping(x-2, y-2, x+2, y+2):
                if item in self.canvas.tri_to_rect:
                    self.handle_tri_click(item)
                    return
            return

        # 检测三角
        for item in self.canvas.find_overlapping(x-2, y-2, x+2, y+2):
            if item in self.canvas.tri_to_rect:
                self.handle_tri_click(item)
                return

        # 检测钉子拖动
        for n in self.nails:
            if math.hypot(x - n.x, y - n.y) <= n.radius + 5:
                self.drag_nail = n
                self.drag_offset_x = x - n.x
                self.drag_offset_y = y - n.y
                return

        # 检测手绘线拖动（直接左键点击拖动）
        items = self.canvas.find_overlapping(x-2, y-2, x+2, y+2)
        for item in items:
            for lid, *rest in self.lines:
                if item == lid and lid in self.freehand_data:
                    # 直接选中并开始拖动
                    for obj in self.selected_objects:
                        if isinstance(obj, Shape):
                            obj.selected = False
                            obj.set_outline(obj.outline)
                            obj.remove_mg_line()
                        elif isinstance(obj, Nail):
                            obj.set_selected(False)
                        elif isinstance(obj, int):
                            self.canvas.itemconfig(obj, fill='black')
                    self.selected_objects = [lid]
                    self.drag_line_id = lid
                    self.drag_offset_x = x - self.freehand_data[lid][0][0]
                    self.drag_offset_y = y - self.freehand_data[lid][0][1]
                    self.canvas.itemconfig(lid, fill='blue')
                    return

        # 检测图形或钉子选中（Ctrl多选）
        # 先找图形
        for s in reversed(self.shapes):
            if self.is_point_in_shape(x, y, s):
                if e.state & 0x0004:  # Ctrl
                    if s in self.selected_objects:
                        self.selected_objects.remove(s)
                        s.selected = False
                        s.set_outline(s.outline)
                        s.remove_mg_line()
                    else:
                        self.selected_objects.append(s)
                        s.selected = True
                        s.set_outline("yellow")
                        s.update_mg_line()
                    return
                else:
                    # 取消其他选中
                    for obj in self.selected_objects:
                        if isinstance(obj, Shape):
                            obj.selected = False
                            obj.set_outline(obj.outline)
                            obj.remove_mg_line()
                        elif isinstance(obj, Nail):
                            obj.set_selected(False)
                        elif isinstance(obj, int):
                            self.canvas.itemconfig(obj, fill='black')
                    self.selected_objects = [s]
                    s.selected = True
                    s.set_outline("yellow")
                    s.update_mg_line()
                    self.drag_shape = s
                    self.drag_offset_x = x - s.x
                    self.drag_offset_y = y - s.y
                    s.is_dragging = True
                    if s.pinned_nail:
                        s.pinned_nail.pinned_shape = None
                        s.pinned_nail = None
                        s.set_outline("black")
                    return
        # 检测钉子（点击空白处取消选中）
        for n in self.nails:
            if math.hypot(x - n.x, y - n.y) <= n.radius + 5:
                if e.state & 0x0004:
                    if n in self.selected_objects:
                        self.selected_objects.remove(n)
                        n.set_selected(False)
                    else:
                        self.selected_objects.append(n)
                        n.set_selected(True)
                    return
                else:
                    # 单选钉子
                    for obj in self.selected_objects:
                        if isinstance(obj, Shape):
                            obj.selected = False
                            obj.set_outline(obj.outline)
                            obj.remove_mg_line()
                        elif isinstance(obj, Nail):
                            obj.set_selected(False)
                        elif isinstance(obj, int):
                            self.canvas.itemconfig(obj, fill='black')
                    self.selected_objects = [n]
                    n.set_selected(True)
                    self.drag_nail = n
                    self.drag_offset_x = x - n.x
                    self.drag_offset_y = y - n.y
                    return

        # 空白取消选中
        for obj in self.selected_objects:
            if isinstance(obj, Shape):
                obj.selected = False
                obj.set_outline(obj.outline)
                obj.remove_mg_line()
            elif isinstance(obj, Nail):
                obj.set_selected(False)
            elif isinstance(obj, int):
                self.canvas.itemconfig(obj, fill='black')
        self.selected_objects = []

    def is_point_in_shape(self, x, y, s):
        if isinstance(s, RectObject):
            return abs(x - s.x) <= s.w/2 and abs(y - s.y) <= s.h/2
        else:
            return math.hypot(x - s.x, y - s.y) <= s.r

    def on_left_drag(self, e):
        if self.drag_nail:
            nx, ny = e.x - self.drag_offset_x, e.y - self.drag_offset_y
            self.drag_nail.update_position(nx, ny)
            self.update_lines_for_nail(self.drag_nail)
            return

        if self.drag_shape:
            self.drag_occurred = True
            dx, dy = e.x - self.drag_offset_x - self.drag_shape.x, e.y - self.drag_offset_y - self.drag_shape.y
            # 移动所有选中的对象（图形和钉子）
            for obj in self.selected_objects:
                if isinstance(obj, Shape):
                    obj.update_position(obj.x + dx, obj.y + dy)
                    self.update_lines_for_shape(obj)
                elif isinstance(obj, Nail):
                    obj.update_position(obj.x + dx, obj.y + dy)
                    self.update_lines_for_nail(obj)
                elif isinstance(obj, int):  # 手绘线
                    if obj in self.freehand_data:
                        points = self.freehand_data[obj]
                        new_points = [(px + dx, py + dy) for px, py in points]
                        self.freehand_data[obj] = new_points
                        flat = [coord for p in new_points for coord in p]
                        self.canvas.coords(obj, *flat)
                        self.canvas.update_idletasks()
            self.drag_offset_x = e.x - self.drag_shape.x
            self.drag_offset_y = e.y - self.drag_shape.y
            near = any(math.hypot(self.drag_shape.x - n.x, self.drag_shape.y - n.y) < self.drag_shape.radius + n.radius + 5
                       for n in self.nails)
            for s in self.selected_objects:
                if isinstance(s, Shape):
                    s.set_outline("yellow" if near else "black")
            return

        # 拖动手绘线
        if self.drag_line_id is not None:
            dx = e.x - self.drag_offset_x - self.freehand_data[self.drag_line_id][0][0]
            dy = e.y - self.drag_offset_y - self.freehand_data[self.drag_line_id][0][1]
            points = self.freehand_data[self.drag_line_id]
            new_points = [(px + dx, py + dy) for px, py in points]
            self.freehand_data[self.drag_line_id] = new_points
            flat = [coord for p in new_points for coord in p]
            self.canvas.coords(self.drag_line_id, *flat)
            self.canvas.update_idletasks()
            self.drag_offset_x = e.x - new_points[0][0]
            self.drag_offset_y = e.y - new_points[0][1]

    def on_left_up(self, e):
        if self.drag_nail:
            self.drag_nail = None
            return

        if self.drag_shape:
            if self.drag_shape.canvas.itemcget(self.drag_shape.rect_id, "outline") == "yellow":
                for n in self.nails:
                    if math.hypot(self.drag_shape.x - n.x, self.drag_shape.y - n.y) < self.drag_shape.radius + n.radius + 5:
                        self.drag_shape.pinned_nail = n
                        n.pinned_shape = self.drag_shape
                        self.drag_shape.set_outline("green")
                        break

            for obj in self.selected_objects:
                if isinstance(obj, Shape):
                    obj.is_dragging = False
                    if obj.pinned_nail is None:
                        obj.vx = obj.vy = 0.0
                        obj.set_outline(obj.outline)
                    else:
                        obj.set_outline("green")

            if not self.drag_occurred and len(self.selected_objects) == 1 and isinstance(self.drag_shape, Shape):
                self.edit_shape_text(self.drag_shape)

            self.drag_shape = None
            self.drag_offset_x = self.drag_offset_y = 0

        # 手绘线拖动结束
        if self.drag_line_id is not None:
            self.drag_line_id = None
            self.drag_offset_x = self.drag_offset_y = 0

    # ===================== 右键菜单 =====================
    def on_right_click(self, e):
        x, y = e.x, e.y
        if self.start_tri:
            self.cancel_temp_line()
            return

        # 检测钉子
        for n in self.nails:
            if math.hypot(x - n.x, y - n.y) <= n.radius + 5:
                self.right_click_nail = n
                self.right_click_shape = None
                self.context_menu.entryconfig(0, state="disabled")
                self.context_menu.entryconfig(1, state="disabled")
                self.context_menu.entryconfig(2, state="normal")
                self.context_menu.entryconfig(3, state="normal")
                self.context_menu.entryconfig(4, state="normal")
                self.context_menu.entryconfig(6, state="disabled")
                self.context_menu.entryconfig(7, state="disabled")
                self.context_menu.entryconfig(9, state="disabled")
                self.context_menu.entryconfig(11, state="normal")
                self.context_menu.post(e.x_root, e.y_root)
                return

        # 检测图形
        for s in reversed(self.shapes):
            if self.is_point_in_shape(x, y, s):
                self.right_click_shape = s
                self.right_click_nail = None
                self.context_menu.entryconfig(0, state="disabled")
                self.context_menu.entryconfig(1, state="disabled")
                self.context_menu.entryconfig(2, state="disabled")
                self.context_menu.entryconfig(3, state="disabled")
                self.context_menu.entryconfig(4, state="disabled")
                self.context_menu.entryconfig(6, state="normal")
                self.context_menu.entryconfig(7, state="normal")
                self.context_menu.entryconfig(9, state="normal")
                self.context_menu.entryconfig(11, state="normal")
                self.context_menu.post(e.x_root, e.y_root)
                return

        # 空白处
        self.right_click_shape = self.right_click_nail = None
        self.context_menu.entryconfig(0, state="normal")
        self.context_menu.entryconfig(1, state="normal")
        self.context_menu.entryconfig(2, state="disabled")
        self.context_menu.entryconfig(3, state="disabled")
        self.context_menu.entryconfig(4, state="disabled")
        self.context_menu.entryconfig(6, state="disabled")
        self.context_menu.entryconfig(7, state="disabled")
        self.context_menu.entryconfig(9, state="normal")
        self.context_menu.entryconfig(11, state="normal")
        self.context_click_pos = (x, y)
        self.context_menu.post(e.x_root, e.y_root)

    def on_right_click_canvas(self, e):
        if self.start_tri:
            self.cancel_temp_line()

    # ===================== 创建图形 =====================
    def create_center_rect(self):
        x, y = self.context_click_pos
        self.shapes.append(RectObject(self.canvas, x, y, 80, 40, fill="white", outline="black"))

    def create_outer_rect(self):
        x, y = self.context_click_pos
        self.shapes.append(RectObject(self.canvas, x, y, 60, 30, fill="lightblue", outline="black"))

    def create_custom_rect(self):
        x, y = self.context_click_pos
        w = simpledialog.askinteger(self.lang['resize_rect_title'], self.lang['resize_rect_prompt_w'], initialvalue=80)
        if w is None: return
        h = simpledialog.askinteger(self.lang['resize_rect_title'], self.lang['resize_rect_prompt_h'], initialvalue=40)
        if h is None: return
        self.shapes.append(RectObject(self.canvas, x, y, w, h, fill="white", outline="black"))

    def create_circle(self):
        x, y = self.context_click_pos
        r = simpledialog.askinteger(self.lang['resize_circle_title'], self.lang['resize_circle_prompt'], initialvalue=30)
        if r is None: return
        self.shapes.append(CircleObject(self.canvas, x, y, r, fill="lightgreen", outline="black"))

    def create_nail(self):
        x, y = self.context_click_pos
        self.nails.append(Nail(self.canvas, x, y))
        self.refresh_layers()

    # ===================== 删除/修改 =====================
    def delete_shape(self, shape):
        if shape.pinned_nail:
            shape.pinned_nail.pinned_shape = None
            shape.pinned_nail = None
        to_remove = []
        for idx, (lid, s1, d1, s2, d2, lt, cid, sl) in enumerate(self.lines):
            if (isinstance(s1, Shape) and s1 is shape) or (isinstance(s2, Shape) and s2 is shape):
                self.canvas.delete(lid)
                if cid:
                    self.canvas.delete(cid)
                to_remove.append(idx)
        for idx in reversed(to_remove):
            del self.lines[idx]
        shape.delete()
        self.shapes.remove(shape)
        if shape in self.selected_objects:
            self.selected_objects.remove(shape)
        self.right_click_shape = None

    def delete_nail(self, nail):
        if nail.pinned_shape:
            nail.pinned_shape.pinned_nail = None
            nail.pinned_shape.set_outline("black")
            nail.pinned_shape.vy = nail.pinned_shape.vx = 0.0
        nail.delete()
        self.nails.remove(nail)
        if nail in self.selected_objects:
            self.selected_objects.remove(nail)

    def delete_selected_shape(self):
        if self.right_click_shape:
            if messagebox.askyesno(self.lang['confirm_delete_shape'], self.lang['confirm_delete_shape_msg']):
                self.delete_shape(self.right_click_shape)

    def resize_selected_shape(self):
        s = self.right_click_shape
        if not s: return
        if hasattr(s, 'w'):
            w = simpledialog.askinteger(self.lang['resize_rect_title'], self.lang['resize_rect_prompt_w'], initialvalue=s.w)
            if w is None: return
            h = simpledialog.askinteger(self.lang['resize_rect_title'], self.lang['resize_rect_prompt_h'], initialvalue=s.h)
            if h is None: return
            s.set_size(w, h)
            self.update_lines_for_shape(s)
        else:
            r = simpledialog.askinteger(self.lang['resize_circle_title'], self.lang['resize_circle_prompt'], initialvalue=s.r)
            if r is None: return
            s.set_radius(r)
            self.update_lines_for_shape(s)

    def resize_nail(self):
        n = self.right_click_nail
        if not n: return
        r = simpledialog.askinteger(self.lang['resize_nail_title'], self.lang['resize_nail_prompt'], initialvalue=n.radius)
        if r is None: return
        n.set_radius(r)

    def delete_selected_nail(self):
        n = self.right_click_nail
        if not n: return
        if messagebox.askyesno(self.lang['confirm_delete_nail'], self.lang['confirm_delete_nail_msg']):
            self.delete_nail(n)
            self.right_click_nail = None

    def start_line_from_nail(self):
        n = self.right_click_nail
        if not n: return
        if self.start_tri:
            self.cancel_temp_line()
        self.start_tri = (n, 'center')
        x0, y0 = n.get_anchor()
        self.temp_line = self.canvas.create_line(x0, y0, x0, y0, fill='black', width=2, dash=(4,2))

    def finish_line_to_nail(self, nail):
        if not self.start_tri or not self.temp_line:
            return
        start_obj, start_dir = self.start_tri
        end_obj = nail
        end_dir = 'center'
        x1, y1 = start_obj.get_anchor(start_dir) if isinstance(start_obj, Shape) else start_obj.get_anchor()
        x2, y2 = end_obj.get_anchor()
        if self.line_type == 'straight':
            lid = self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
            cid = None
        elif self.line_type == 'curve':
            cx, cy = (x1+x2)/2, (y1+y2)/2 - 30
            lid = self.canvas.create_line(x1, y1, cx, cy, x2, y2, fill='black', width=2, smooth=True)
            cid = self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill='red', outline='red')
            self.canvas.tag_bind(cid, "<B1-Motion>", lambda e, lid=lid, cid=cid: self.on_control_drag(e, lid, cid))
        else:
            lid = self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
            cid = None
        self.lines.append((lid, start_obj, start_dir, end_obj, end_dir, self.line_type, cid, None))
        self.canvas.tag_bind(lid, "<Button-3>", lambda e, lid=lid: self.on_line_right_click(e, lid))
        self.canvas.delete(self.temp_line)
        self.temp_line = None
        self.start_tri = None
        self.refresh_layers()

    # ===================== 图层刷新 =====================
    def refresh_layers(self):
        for s in self.shapes:
            if s.rect_id:
                self.canvas.tag_lower(s.rect_id)
            if s.text_id:
                self.canvas.tag_lower(s.text_id)
            if s.tri_left:
                self.canvas.tag_lower(s.tri_left)
            if s.tri_right:
                self.canvas.tag_lower(s.tri_right)
            if s.mg_line:
                self.canvas.tag_lower(s.mg_line)
            if s.mg_arrow:
                self.canvas.tag_lower(s.mg_arrow)
        for lid, *rest in self.lines:
            self.canvas.tag_lower(lid)
        for lid, *rest in self.lines:
            self.canvas.tag_raise(lid)
        for n in self.nails:
            self.canvas.tag_raise(n.circle_id)
        for s in self.shapes:
            if s.text_id:
                self.canvas.tag_raise(s.text_id)

    def edit_shape_text(self, s):
        txt = simpledialog.askstring(self.lang['input_text_title'], self.lang['input_text_prompt'], initialvalue=s.text)
        if txt is not None:
            s.text = txt
            if s.text_id:
                self.canvas.itemconfig(s.text_id, text=txt)
                self.canvas.tag_raise(s.text_id)
            else:
                s.text_id = self.canvas.create_text(s.x, s.y, text=txt, font=("Arial", 10))
                self.canvas.tag_raise(s.text_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()