# Copyright (C) 2020 Logan Bier. All rights reserved.
# this program is in development
# this is an unofficial and preliminary adaptation
# of panda3d-simplepbr (license file in /)
# https://github.com/Moguri/panda3d-simplepbr/issues/2

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import sys
from panda3d.core import LPoint3f, Point3, Vec3
from panda3d.core import WindowProperties
# gui imports
from direct.gui.DirectGui import *
from panda3d.core import TextNode
import random
# new pbr imports
import simplepbr
import gltf
# local imports
import actor_ai


class app(ShowBase):
    def __init__(self):
        load_prc_file_data("", """
            win-size 1920 1080
            show-frame-rate-meter #t
            view-frustum-cull 0
            textures-power-2 none
            gl-depth-zero-to-one true
            hardware-animated-vertices true
            basic-shaders-only false
            loader-num-threads 24
            frame-rate-meter-milliseconds true
            window-title PBR Hardware Skinning Demo
            fullscreen #f
        """)
        
        # Initialize the showbase
        super().__init__()
        pipeline = simplepbr.init()
        pipeline.enable_shadows = False
        pipeline.max_lights = 10
        gltf.patch_loader(self.loader)
        
        self.accept("escape", sys.exit, [0])
        
        self.cam.setPos(-10, 10, 3)
        self.cam.lookAt(0, 0, 0)
        
        amb_light = AmbientLight('amblight')
        amb_light.setColor((0.2, 0.2, 0.2, 1))
        amb_light_node = self.render.attachNewNode(amb_light)
        self.render.setLight(amb_light_node)

        p_light = Spotlight('p_light')
        p_light.setColor((1, 1, 1, 1))
        p_light.setShadowCaster(True, 1024, 1024)
        lens = PerspectiveLens()
        p_light.setLens(lens)
        p_light_node = self.render.attachNewNode(p_light)
        p_light_node.setPos(-5, -5, 5)
        p_light_node.lookAt(0, 0, 0)
        self.render.setLight(p_light_node)
        
        #############################################
        # reparent player character to render node
        char_body = actor_ai.tilter
        char_body.reparent_to(self.render)
        char_body.setScale(1)
        
        # prototype hardware skinning shader for Actor nodes
        actor_shader = Shader.load(Shader.SL_GLSL, "shaders/simplepbr_vert_mod_1.vert", "shaders/simplepbr_frag_mod_1.frag")
        actor_shader = ShaderAttrib.make(actor_shader)
        # actor_shader = actor_shader.setFlag(ShaderAttrib.F_hardware_skinning, True)
        # char_body.setShaderAuto()
        char_body.setAttrib(actor_shader)
        
        # animate the Actor
        tilt_ctrl = actor_ai.tilter.getAnimControl('wave')
        if not tilt_ctrl.isPlaying():
            actor_ai.tilter.loop('wave')
            actor_ai.tilter.setPlayRate(3.0, 'wave')
        
        def move(Task):
            # print('the scene is updating')
            
            return Task.cont

        self.task_mgr.add(move)

app().run()
