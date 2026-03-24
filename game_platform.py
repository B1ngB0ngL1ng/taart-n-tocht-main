from ursina import *


class Platform:
    def het_platform_om_op_te_springen(
        x_as,
        y_as,
        z_as,
        schaal,
    ):
        Entity(
            model="cube",
            collider="box",
            texture="brick",
            scale=schaal,
            x=x_as,
            y=y_as,
            z=z_as,
        )
