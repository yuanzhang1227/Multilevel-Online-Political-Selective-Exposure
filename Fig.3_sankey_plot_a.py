# importing the required module
import plotly.graph_objects as go

label=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22',
               'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46',
               'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14',
               'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
               'D1', 'D2', 'D3',
               'E1', 'E2']
data = [
    {"source": 'A5', "target": 'B1', "value": 2},
    {"source": 'A8', "target": 'B1', "value": 87},
    {"source": 'A10', "target": 'B1', "value": 78},
    {"source": 'A11', "target": 'B1', "value": 2},
    {"source": 'A16', "target": 'B1', "value": 56},
    {"source": 'A17', "target": 'B1', "value": 23},
    {"source": 'A18', "target": 'B1', "value": 1},
    {"source": 'A19', "target": 'B1', "value": 7},
    {"source": 'A20', "target": 'B1', "value": 51},
    {"source": 'A21', "target": 'B1', "value": 2},
    {"source": 'A22', "target": 'B1', "value": 7},
    {"source": 'A23', "target": 'B1', "value": 3},
    {"source": 'A24', "target": 'B1', "value": 1},
    {"source": 'A25', "target": 'B1', "value": 31},
    {"source": 'A26', "target": 'B1', "value": 14},
    {"source": 'A27', "target": 'B1', "value": 14},
    {"source": 'A28', "target": 'B1', "value": 21},
    {"source": 'A29', "target": 'B1', "value": 23},
    {"source": 'A30', "target": 'B1', "value": 21},
    {"source": 'A34', "target": 'B1', "value": 9},
    {"source": 'A38', "target": 'B1', "value": 1},
    {"source": 'A39', "target": 'B1', "value": 3},
    {"source": 'A44', "target": 'B1', "value": 1},
    {"source": 'A3', "target": 'B2', "value": 2},
    {"source": 'A4', "target": 'B2', "value": 122},
    {"source": 'A6', "target": 'B2', "value": 3},
    {"source": 'A7', "target": 'B2', "value": 2},
    {"source": 'A9', "target": 'B2', "value": 6},
    {"source": 'A13', "target": 'B2', "value": 7},
    {"source": 'A15', "target": 'B2', "value": 5},
    {"source": 'A16', "target": 'B2', "value": 2},
    {"source": 'A17', "target": 'B2', "value": 3},
    {"source": 'A18', "target": 'B2', "value": 48},
    {"source": 'A19', "target": 'B2', "value": 9},
    {"source": 'A22', "target": 'B2', "value": 1},
    {"source": 'A23', "target": 'B2', "value": 22},
    {"source": 'A24', "target": 'B2', "value": 1},
    {"source": 'A25', "target": 'B2', "value": 1},
    {"source": 'A30', "target": 'B2', "value": 1},
    {"source": 'A31', "target": 'B2', "value": 1},
    {"source": 'A32', "target": 'B2', "value": 17},
    {"source": 'A39', "target": 'B2', "value": 1},
    {"source": 'A40', "target": 'B2', "value": 3},
    {"source": 'A43', "target": 'B2', "value": 1},
    {"source": 'A45', "target": 'B2', "value": 1},
    {"source": 'A46', "target": 'B2', "value": 1},
    {"source": 'A5', "target": 'B3', "value": 102},
    {"source": 'A12', "target": 'B3', "value": 73},
    {"source": 'A17', "target": 'B3', "value": 10},
    {"source": 'A19', "target": 'B3', "value": 2},
    {"source": 'A21', "target": 'B3', "value": 39},
    {"source": 'A22', "target": 'B3', "value": 8},
    {"source": 'A26', "target": 'B3', "value": 8},
    {"source": 'A36', "target": 'B3', "value": 7},
    {"source": 'A1', "target": 'B4', "value": 194},
    {"source": 'A5', "target": 'B4', "value": 3},
    {"source": 'A12', "target": 'B4', "value": 1},
    {"source": 'A17', "target": 'B4', "value": 1},
    {"source": 'A27', "target": 'B4', "value": 1},
    {"source": 'A5', "target": 'B5', "value": 3},
    {"source": 'A6', "target": 'B5', "value": 8},
    {"source": 'A7', "target": 'B5', "value": 98},
    {"source": 'A8', "target": 'B5', "value": 2},
    {"source": 'A9', "target": 'B5', "value": 2},
    {"source": 'A10', "target": 'B5', "value": 1},
    {"source": 'A11', "target": 'B5', "value": 3},
    {"source": 'A13', "target": 'B5', "value": 1},
    {"source": 'A18', "target": 'B5', "value": 7},
    {"source": 'A19', "target": 'B5', "value": 1},
    {"source": 'A20', "target": 'B5', "value": 4},
    {"source": 'A21', "target": 'B5', "value": 1},
    {"source": 'A22', "target": 'B5', "value": 1},
    {"source": 'A23', "target": 'B5', "value": 10},
    {"source": 'A26', "target": 'B5', "value": 6},
    {"source": 'A27', "target": 'B5', "value": 1},
    {"source": 'A28', "target": 'B5', "value": 6},
    {"source": 'A32', "target": 'B5', "value": 1},
    {"source": 'A38', "target": 'B5', "value": 4},
    {"source": 'A41', "target": 'B5', "value": 1},
    {"source": 'A3', "target": 'B6', "value": 136},
    {"source": 'A16', "target": 'B6', "value": 1},
    {"source": 'A31', "target": 'B6', "value": 1},
    {"source": 'A35', "target": 'B6', "value": 8},
    {"source": 'A2', "target": 'B7', "value": 140},
    {"source": 'A11', "target": 'B7', "value": 1},
    {"source": 'A13', "target": 'B7', "value": 1},
    {"source": 'A15', "target": 'B7', "value": 2},
    {"source": 'A42', "target": 'B7', "value": 1},
    {"source": 'A6', "target": 'B8', "value": 93},
    {"source": 'A15', "target": 'B8', "value": 1},
    {"source": 'A17', "target": 'B8', "value": 11},
    {"source": 'A19', "target": 'B8', "value": 20},
    {"source": 'A21', "target": 'B8', "value": 10},
    {"source": 'A23', "target": 'B8', "value": 1},
    {"source": 'A13', "target": 'B9', "value": 62},
    {"source": 'A15', "target": 'B9', "value": 55},
    {"source": 'A27', "target": 'B9', "value": 12},
    {"source": 'A5', "target": 'B10', "value": 2},
    {"source": 'A8', "target": 'B10', "value": 4},
    {"source": 'A9', "target": 'B10', "value": 79},
    {"source": 'A11', "target": 'B10', "value": 1},
    {"source": 'A17', "target": 'B10', "value": 8},
    {"source": 'A22', "target": 'B10', "value": 29},
    {"source": 'A5', "target": 'B11', "value": 1},
    {"source": 'A11', "target": 'B11', "value": 68},
    {"source": 'A19', "target": 'B11', "value": 16},
    {"source": 'A29', "target": 'B11', "value": 2},
    {"source": 'A31', "target": 'B11', "value": 19},
    {"source": 'A37', "target": 'B11', "value": 7},
    {"source": 'A14', "target": 'B12', "value": 69},
    {"source": 'A24', "target": 'B13', "value": 31},
    {"source": 'A33', "target": 'B14', "value": 17},
    {"source": 'B1', "target": 'C1', "value": 458},
    {"source": 'B2', "target": 'C1', "value": 257},
    {"source": 'B3', "target": 'C1', "value": 162},
    {"source": 'B4', "target": 'C1', "value": 1},
    {"source": 'B5', "target": 'C1', "value": 161},
    {"source": 'B6', "target": 'C1', "value": 2},
    {"source": 'B7', "target": 'C1', "value": 2},
    {"source": 'B8', "target": 'C1', "value": 136},
    {"source": 'B9', "target": 'C1', "value": 77},
    {"source": 'B10', "target": 'C1', "value": 123},
    {"source": 'B11', "target": 'C1', "value": 113},
    {"source": 'B14', "target": 'C1', "value": 17},
    {"source": 'B2', "target": 'C2', "value": 3},
    {"source": 'B6', "target": 'C2', "value": 144},
    {"source": 'B7', "target": 'C2', "value": 143},
    {"source": 'B9', "target": 'C2', "value": 52},
    {"source": 'B3', "target": 'C3', "value": 1},
    {"source": 'B4', "target": 'C3', "value": 199},
    {"source": 'B3', "target": 'C4', "value": 73},
    {"source": 'B12', "target": 'C5', "value": 69},
    {"source": 'B13', "target": 'C6', "value": 31},
    {"source": 'B3', "target": 'C7', "value": 7},
    {"source": 'B3', "target": 'C8', "value": 6},
    {"source": 'C1', "target": 'D1', "value": 1509},
    {"source": 'C2', "target": 'D1', "value": 342},
    {"source": 'C3', "target": 'D1', "value": 1},
    {"source": 'C4', "target": 'D1', "value": 73},
    {"source": 'C6', "target": 'D1', "value": 31},
    {"source": 'C7', "target": 'D1', "value": 7},
    {"source": 'C8', "target": 'D1', "value": 6},
    {"source": 'C3', "target": 'D2', "value": 199},
    {"source": 'C5', "target": 'D3', "value": 69},
    {"source": 'D1', "target": 'E1', "value": 1969},
    {"source": 'D2', "target": 'E1', "value": 199},
    {"source": 'D3', "target": 'E2', "value": 69}
]

ideology_left_50 = ['A2','A3','A4','A13','A39','B2','B6','B7','C2']
ideology_right_50 = ['A1','A12','B3','B4','C3','C4','D2']
ideology_center_50 = []
ideology_mixed_50 = ['A5', 'A11',]

ideology_left_30 = ['A9','A15','A18','A23','A32','B9']
ideology_right_30 = ['A36','C7']
ideology_center_30 = []
ideology_mixed_30 = ['A17','A21','A28','B10','B11','C1','D1','E1']

ideology_left_10 = ['A6','A8','A25','A31','A34','A37','A38','B8','B13','C6']
ideology_right_10 = ['A14','B12','C5','D3','E2']
ideology_center_10 = []
ideology_mixed_10 = ['A7','A19','A22','A24','A27','A29','B1','B5',]

def get_color(label):
    red_no_transparency = 'rgba(255, 0, 0, 0.8)'    # No transparency
    red_medium_transparency = 'rgba(255, 0, 0, 0.5)'  # Medium transparency
    red_high_transparency = 'rgba(255, 0, 0, 0.2)'   # High transparency

    # Blue
    blue_no_transparency = 'rgba(0, 0, 255, 0.8)'   # No transparency
    blue_medium_transparency = 'rgba(0, 0, 255, 0.5)' # Medium transparency
    blue_high_transparency = 'rgba(0, 0, 255, 0.2)'  # High transparency

    # Orange
    orange_no_transparency = 'rgba(255, 165, 0, 0.8)'  # No transparency
    orange_medium_transparency = 'rgba(255, 165, 0, 0.5)' # Medium transparency
    orange_high_transparency = 'rgba(255, 165, 0, 0.2)'  # High transparency

    if label in ideology_left_50:
        return red_no_transparency
    elif label in ideology_left_30:
        return red_medium_transparency
    elif label in ideology_left_10:
        return red_high_transparency

    if label in ideology_right_50:
        return blue_no_transparency
    elif label in ideology_right_30:
        return blue_medium_transparency
    elif label in ideology_right_10:
        return blue_high_transparency

    if label in ideology_center_50:
        return orange_no_transparency
    elif label in ideology_center_30:
        return orange_medium_transparency
    elif label in ideology_center_10:
        return orange_high_transparency

    else:
        return 'grey'

def get_link_color(source_label):
    link_colors = {
        'ideology_left': {
            50: 'rgba(255, 0, 0, 0.7)',
            30: 'rgba(255, 0, 0, 0.4)',
            10: 'rgba(255, 0, 0, 0.1)'
        },
        'ideology_right': {
            50: 'rgba(0, 0, 255, 0.7)',
            30: 'rgba(0, 0, 255, 0.4)',
            10: 'rgba(0, 0, 255, 0.1)',
        },
        'ideology_center': {
            50: 'rgba(255, 165, 0, 0.7)',
            30: 'rgba(255, 165, 0, 0.4)',
            10: 'rgba(255, 165, 0, 0.1)',
        }
    }

    # Determine link color based on source category and level
    for group, levels in link_colors.items():
        for level, color in levels.items():
            if source_label in globals()[f'{group}_{level}']:
                return color

    return 'rgba(169, 169, 169, 0.5)'

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=30,
        thickness=50,
        line=dict(color="black", width=1),
        label=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22',
               'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46',
               'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14',
               'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
               'D1', 'D2', 'D3',
               'E1', 'E2'],
        color=[get_color(label) for label in
               ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22',
                'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46',
                'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14',
                'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
                'D1', 'D2', 'D3',
                'E1', 'E2']]
    ),
    link=dict(
        source=[label.index(item['source']) for item in data],
        target=[label.index(item['target']) for item in data],
        value=[item['value'] for item in data],
        # color=['rgba(255, 182, 193, 0.5)' if item['source'] in social_religious else 'rgba(144, 238, 144, 0.5)' if item['source'] in social_women else 'rgba(128, 0, 128, 0.5)' if item['source'] in social_lgbtq else 'rgba(169, 169, 169, 0.5)' for item in data]
        color = [get_link_color(item['source']) for item in data]
    )
)])

# Add a dummy trace for each color category
colors = {'red': 'Left', 'blue': 'Right', 'orange': 'Center'}
for color, label in colors.items():
    fig.add_trace(go.Scatter(mode='markers', x=[None], y=[None], marker=dict(color=color), name=label))

fig.update_layout(
    font=dict(size=40),
    width=2000,
    height=1600,
    title_x=0.5,

    xaxis=dict(
        tickvals=[],
        ticktext=[]
    ),
    yaxis=dict(
        tickvals=[],
        ticktext=[]
    ),
    legend=dict(
        x=0.846,
        y=1,
        traceorder='normal',
        tracegroupgap=10,
        font=dict(size=50
        ),
        bgcolor="WhiteSmoke",
        itemsizing = "constant",
        itemwidth = 100
    ),

    annotations=[

        dict(
            x=0.00,
            y=1.05,
            xref='paper',
            yref='paper',
            text='Level 1',
            showarrow=False,
            font=dict(size=60)
        ),

        dict(
            x=0.23,
            y=1.05,
            xref='paper',
            yref='paper',
            text='Level 2',
            showarrow=False,
            font=dict(size=60)
        ),

        dict(
            x=0.5,
            y=1.05,
            xref='paper',
            yref='paper',
            text='Level 3',
            showarrow=False,
            font=dict(size=60)
        ),

        dict(
            x=0.77,
            y=1.05,
            xref='paper',
            yref='paper',
            text='Level 4',
            showarrow=False,
            font=dict(size=60)
        ),

        dict(
            x=1,
            y=1.05,
            xref='paper',
            yref='paper',
            text='Level 5',
            showarrow=False,
            font=dict(size=60)
        ),
    ]
)

fig.show()