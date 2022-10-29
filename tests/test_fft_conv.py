import jax.numpy as jnp
import numpy.testing as npt

import serket.experimental as ske


def test_fft_conv1d():
    x = jnp.array(
        [
            [0.01575461, -0.7551311, 1.6749918, 2.0053358, -0.77692, 0.24808577],
            [-0.13778068, 0.33827955, -0.7429483, -0.29843795, 0.7299512, 0.07700217],
        ]
    )

    b = jnp.array(
        [
            [0.18520592],
            [1.4190177],
            [-0.40039113],
            [-0.01156754],
            [-0.63538706],
            [-0.14201863],
        ]
    )

    w = jnp.array(
        [
            [[1.184718, -1.5479481, -0.30058688]],
            [[0.73833615, 0.88512796, 0.04418173]],
            [[0.6661497, -0.9757734, -1.2271975]],
            [[-2.0575454, 0.7450601, 1.3366221]],
            [[-0.91172457, 0.820197, 0.75473523]],
            [[0.47344425, -0.2698045, 0.08849244]],
        ]
    )

    layer = ske.FFTConv1D(2, 6, kernel_size=3, padding=0, strides=1, groups=2)
    layer = layer.at["weight"].set(w)
    layer = layer.at["bias"].set(b)

    y = jnp.array(
        [
            [0.8692938, -3.9049897, -0.7010245, 3.689024],
            [0.8362662, 2.4326584, 4.3963776, 2.2229166],
            [-1.7086053, -4.998777, -0.28791457, 1.3891104],
            [-0.46908, -1.660033, 2.270397, 1.2492625],
            [-0.7930424, -1.7784103, 0.34811908, 0.29352617],
            [-0.3642648, 0.19217919, -0.34864813, -0.47344238],
        ]
    )

    npt.assert_allclose(y, layer(x), atol=1e-4)


def test_fft_conv2d():

    x = jnp.array(
        [
            [
                [
                    -0.549542,
                    -1.3339283,
                    0.8833371,
                    0.5553847,
                    0.47893846,
                    1.1174014,
                ],
                [
                    -0.22968262,
                    0.11734157,
                    -0.14974171,
                    0.6963892,
                    0.788569,
                    -0.3478001,
                ],
                [
                    0.2226113,
                    1.1436108,
                    0.35447085,
                    0.574005,
                    -0.09518735,
                    1.5748154,
                ],
                [
                    -1.1870643,
                    1.2478359,
                    -0.3521663,
                    -1.1033075,
                    -0.66324735,
                    2.3269835,
                ],
                [
                    0.9641067,
                    1.5799146,
                    2.6478772,
                    0.9201643,
                    -0.29368097,
                    -0.40184128,
                ],
                [
                    0.31325057,
                    -0.4772391,
                    0.7948965,
                    -0.7406322,
                    -0.6040924,
                    -0.37352082,
                ],
            ],
            [
                [
                    -0.06433684,
                    0.7014926,
                    -0.3051094,
                    -0.5549095,
                    -1.208778,
                    0.23271216,
                ],
                [
                    -0.68725157,
                    -0.16840899,
                    -0.14859934,
                    0.24689208,
                    0.39400205,
                    -2.0993593,
                ],
                [
                    -0.8641717,
                    -0.14099717,
                    -1.1759962,
                    -0.08090389,
                    0.8530338,
                    -1.9193401,
                ],
                [
                    -0.38752368,
                    0.91806966,
                    -1.2521442,
                    0.6852556,
                    0.5300909,
                    -1.0087785,
                ],
                [
                    1.1596189,
                    0.30318046,
                    -0.82135236,
                    1.4496957,
                    -1.0101783,
                    -0.4048503,
                ],
                [
                    -1.2882348,
                    0.83471847,
                    -0.12463568,
                    0.8996316,
                    -1.6368964,
                    0.92466456,
                ],
            ],
        ]
    )

    w = jnp.array(
        [
            [
                [
                    [-2.4534044, -0.94401747, -0.7787958],
                    [0.82851595, -0.83861977, -0.67498463],
                    [-2.6933532, -0.45811504, 1.3679986],
                ]
            ],
            [
                [
                    [-0.5673468, 1.5330081, 0.5192263],
                    [-1.0009775, -1.4451538, 0.0209155],
                    [-0.45217156, -0.8792319, 1.5607767],
                ]
            ],
            [
                [
                    [-0.13168886, 1.1761682, 0.24837889],
                    [0.5575214, 0.4443017, -1.2817512],
                    [-0.5824908, -0.5981872, -0.46461147],
                ]
            ],
            [
                [
                    [-1.2966781, -0.6955817, 1.563403],
                    [-1.3016162, 0.5792713, 0.10513221],
                    [1.5448943, 1.4904625, -0.8599378],
                ]
            ],
            [
                [
                    [-0.9862045, -0.7823246, -0.49286386],
                    [-0.5642265, 0.15855414, -0.7280983],
                    [-0.33804402, 0.99465144, 0.9627097],
                ]
            ],
            [
                [
                    [0.11336798, -1.067196, -0.00707494],
                    [1.0206488, 0.08515337, -0.5990882],
                    [0.92347324, 2.0158308, 0.12967472],
                ]
            ],
        ]
    )

    b = jnp.array(
        [
            [[-1.4410067]],
            [[-1.8514851]],
            [[0.17418846]],
            [[-1.1783965]],
            [[1.1077121]],
            [[-0.704997]],
        ]
    )

    ls = ske.FFTConv2D(2, 6, kernel_size=3, padding=0, strides=1, groups=2)
    ls = ls.at["weight"].set(w)
    ls = ls.at["bias"].set(b)

    y = jnp.array(
        [
            [
                [-0.347633, -2.1393116, -7.093711, -3.3235703],
                [0.25823128, -6.575943, -1.9219761, 2.3280842],
                [-4.8332357, -7.164022, -9.652208, -8.807953],
                [-1.283464, -4.935389, -0.02659357, 3.1201706],
            ],
            [
                [-3.6216846, 0.72847974, -2.9060965, -0.41404986],
                [-4.5971813, -5.4076347, -1.3817259, 3.0915818],
                [1.6446689, -4.028381, -1.7536781, -0.17887545],
                [-1.1221895, -10.700049, -8.324921, -1.2560662],
            ],
            [
                [-1.9654049, -0.5118289, -0.46039268, 1.117219],
                [0.59176624, 0.21134838, 2.9567754, -0.8589388],
                [-0.81491554, -0.39526203, -1.0137777, -3.6882308],
                [-0.7100501, 0.34608507, 1.2803423, 1.9812675],
            ],
            [
                [-1.8124869, -4.4852757, -4.5796614, 3.2288744],
                [2.3635092, -2.0141025, -0.3368768, -1.940866],
                [2.055932, -4.154777, 5.579398, -4.2763357],
                [-5.3310986, -0.8143792, 5.155924, -8.37253],
            ],
            [
                [0.2617448, -0.38014543, 3.4129033, 2.965688],
                [3.1506543, 0.3242755, 2.5117245, 2.4935036],
                [3.0446048, 1.4673727, 3.08662, 0.0134331],
                [2.5263517, -0.05271554, 2.3351169, -1.2110296],
            ],
            [
                [-3.3202841, -3.1396906, -1.6439965, 3.459662],
                [0.53880435, -2.3502686, -2.4125466, 1.6278615],
                [1.3641498, -0.2332559, -0.2623811, -1.0121444],
                [0.45845002, 0.7377768, -0.20553878, -1.8987479],
            ],
        ]
    )

    npt.assert_allclose(ls(x), y, atol=1e-6)


def test_fft_conv3d():
    x = jnp.array(
        [
            [
                [
                    [-1.3983929, 2.3941393, 0.8059137, 0.25440317],
                    [0.64289266, 0.3687553, 1.0278206, -0.96984893],
                    [-0.13827659, -0.0059691, -0.37837136, 0.23375748],
                    [-0.68457204, -0.577046, 1.3687764, 1.4311088],
                ],
                [
                    [0.9638318, 1.0693446, -1.3602823, -0.06612433],
                    [-0.13134617, 0.59240246, -0.1954011, 0.4358241],
                    [-0.29530987, -0.6959144, 0.12965553, 0.77832645],
                    [-0.6786789, 0.05597273, 0.06958026, 0.52453727],
                ],
                [
                    [-1.8936639, 0.5127249, 0.67948705, 0.62513864],
                    [0.13869773, -0.34793302, -0.2645528, -0.18003541],
                    [-1.2825309, -0.53816295, -0.65780264, 0.3016272],
                    [-1.0797601, -1.6925293, -0.4519003, 0.20517777],
                ],
                [
                    [-0.45080215, 1.2191048, 0.19665839, 0.52653944],
                    [0.37190276, -0.15672162, 1.2273518, 0.15244119],
                    [-0.9072173, -2.3722272, 0.7403431, 0.12519889],
                    [-2.0534873, 0.091593, -1.2043465, -0.55693346],
                ],
            ],
            [
                [
                    [0.5812955, 0.14317094, -0.68801063, 0.08280475],
                    [0.69881725, 1.0819827, -0.46610656, -0.77676356],
                    [0.6404173, -0.4072523, 1.4515287, -0.5243245],
                    [-0.04088914, 0.28167385, 0.09770074, -0.34966195],
                ],
                [
                    [0.03866513, -0.3620568, -0.62257665, 1.663655],
                    [1.803672, -2.3896644, 0.59561074, -0.42770556],
                    [-0.318432, -0.412128, 0.27280888, 0.39802825],
                    [-0.44855025, 1.4048548, -0.9125727, 0.03513884],
                ],
                [
                    [-0.21829003, -0.2197383, -0.42028508, 0.64728373],
                    [0.16848761, 0.09026208, -0.15521993, -2.5493407],
                    [1.1931965, -0.30211183, -1.9345592, -0.31982675],
                    [-1.438272, -2.0968118, -1.150051, 1.0702634],
                ],
                [
                    [-0.5840807, -0.45338133, 1.6384157, -1.5754535],
                    [-0.80601794, 0.8696974, 0.7674778, 0.89319944],
                    [0.30241844, 2.2657022, -0.5469971, -1.1947122],
                    [-0.16910088, 0.42569765, 0.9003221, -0.561269],
                ],
            ],
        ]
    )

    w = jnp.array(
        [
            [
                [
                    [
                        [-2.11135954e-01, 1.21744084e00, -2.48767018e00],
                        [1.83807611e00, 9.89321768e-01, 1.18106508e00],
                        [3.11494082e-01, 6.00763977e-01, -1.20416760e-01],
                    ],
                    [
                        [2.92916566e-01, -3.88592094e-01, -1.35277152e00],
                        [-5.87185919e-01, 8.98038685e-01, -1.17024708e00],
                        [-4.29188192e-01, 7.43641973e-01, -1.03671744e-01],
                    ],
                    [
                        [-5.73784947e-01, -1.57377645e-01, 8.77945185e-01],
                        [-5.03640532e-01, -1.00357378e00, -1.37753558e00],
                        [-5.20533800e-01, 1.17978521e-01, -3.88222456e-01],
                    ],
                ]
            ],
            [
                [
                    [
                        [3.47213298e-01, 4.29560751e-01, 1.91839293e-01],
                        [-3.46923470e-02, 6.21378064e-01, 7.67743409e-01],
                        [-8.97470355e-01, 2.62481779e-01, -1.47381091e00],
                    ],
                    [
                        [-1.60038340e00, -4.14097458e-01, 3.52366626e-01],
                        [7.92069435e-01, 1.65974629e00, -4.00882572e-01],
                        [-6.02983236e-01, -1.09219782e-01, 1.35120368e00],
                    ],
                    [
                        [-5.32949328e-01, 8.20548356e-01, 5.34247279e-01],
                        [3.93234998e-01, 6.09742329e-02, -2.57880054e-02],
                        [-2.36375853e-01, 1.04388487e00, 9.27554488e-01],
                    ],
                ]
            ],
            [
                [
                    [
                        [-1.90078467e-02, -2.55312264e-01, -5.29372573e-01],
                        [1.44607663e00, -5.17290115e-01, -5.80491088e-02],
                        [-7.87345707e-01, 1.04443622e00, -1.13124095e-01],
                    ],
                    [
                        [1.03147829e00, 1.41797042e00, -1.46525890e-01],
                        [-1.85793471e00, 5.74292941e-03, -4.28088188e-01],
                        [6.11036479e-01, -5.65014303e-01, -6.41347289e-01],
                    ],
                    [
                        [2.33281121e-01, -1.31521904e00, 9.99201894e-01],
                        [-3.77649277e-01, 9.96409059e-01, 1.00733590e00],
                        [-1.09864259e00, -1.44162357e00, -5.67822158e-01],
                    ],
                ]
            ],
            [
                [
                    [
                        [6.24387622e-01, 1.01545942e00, -1.22289562e00],
                        [1.46730638e00, -1.57226396e00, 8.75909030e-01],
                        [-4.20855463e-01, -3.66381764e-01, -4.85681981e-01],
                    ],
                    [
                        [1.42229617e00, -1.58617949e00, 2.00688863e00],
                        [1.13818467e00, 9.44225669e-01, 1.91877350e-01],
                        [-8.44177067e-01, 8.34527254e-01, -1.29088712e00],
                    ],
                    [
                        [8.84030938e-01, -5.00528455e-01, -1.05564523e00],
                        [2.58191633e00, 8.84430885e-01, 3.69496047e-01],
                        [-3.96177143e-01, 8.07036519e-01, 1.39247084e00],
                    ],
                ]
            ],
            [
                [
                    [
                        [-1.74483836e00, -3.36244822e-01, -2.06807345e-01],
                        [2.10218444e-01, 3.06858301e-01, -4.96874005e-01],
                        [5.17425351e-02, -8.63649905e-01, -7.77763963e-01],
                    ],
                    [
                        [1.04713368e00, 1.25883305e00, -3.37810755e-01],
                        [-6.00049376e-01, -7.33305275e-01, -1.51510969e-01],
                        [-1.64427352e00, 4.07986939e-01, -4.33313772e-02],
                    ],
                    [
                        [1.22514689e00, 5.94410300e-01, 3.09060246e-01],
                        [-1.83873487e00, 1.95129287e00, 1.34687269e00],
                        [6.81687176e-01, -5.77292144e-01, 7.48371482e-01],
                    ],
                ]
            ],
            [
                [
                    [
                        [2.07250953e00, -3.40789080e00, -2.83971846e-01],
                        [1.95104241e-01, 1.04560578e00, 2.57927412e-03],
                        [9.96985734e-02, -1.13759375e00, -2.92989641e-01],
                    ],
                    [
                        [5.31376779e-01, 9.18255031e-01, -1.31809521e00],
                        [1.37518024e00, -1.91607147e-01, 6.61842883e-01],
                        [1.56074512e00, 1.16708624e00, -1.80119351e-02],
                    ],
                    [
                        [1.24981332e00, 1.01165974e00, 1.26828551e00],
                        [-1.35727465e-01, 3.25082913e-02, -1.66530713e-01],
                        [-1.70908558e00, 1.46950305e00, -3.53784323e-01],
                    ],
                ]
            ],
        ]
    )

    b = jnp.array(
        [
            [[[-0.6961791]]],
            [[[-0.560233]]],
            [[[-0.53402895]]],
            [[[2.1265218]]],
            [[[0.08771288]]],
            [[[-0.5548572]]],
        ]
    )

    y = jnp.array(
        [
            [
                [[8.514449, 0.57268554], [-2.2805903, 3.8453667]],
                [[0.2589906, -2.6648269], [4.353338, -2.0567143]],
            ],
            [
                [[1.6998817, 0.55508506], [-5.8246617, -2.4271045]],
                [[2.6016793, -0.55015504], [-2.509073, -1.6608118]],
            ],
            [
                [[3.905511, -3.4758859], [2.5474095, 4.82761]],
                [[0.79460865, 6.7832074], [5.9190063, -0.41354537]],
            ],
            [
                [[-2.1619222, 1.1835424], [16.17303, -5.7423515]],
                [[8.201732, -4.8360176], [4.358927, -2.5986512]],
            ],
            [
                [[-1.4781605, -3.7855282], [-7.758099, -9.34947]],
                [[-0.5375103, 1.0997473], [1.673322, 4.4247713]],
            ],
            [
                [[1.7628655, -8.410817], [-4.515975, 3.8339481]],
                [[4.94558, -10.983931], [6.97976, -4.002919]],
            ],
        ]
    )

    ls = ske.FFTConv3D(2, 6, kernel_size=3, padding=0, strides=1, groups=2)
    ls = ls.at["weight"].set(w)
    ls = ls.at["bias"].set(b)

    npt.assert_allclose(ls(x), y)
