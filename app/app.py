import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 
import shinyswatch

shinyswatch.theme.minty()

df = palmerpenguins.load_penguins()

ui.page_opts(title="K.young Penguins dashboard", fillable=True)


with ui.sidebar(title="Filter controls", text="blue" ):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "K. Young Project GitHub  Source",
        href="https://github.com/Keyoungg2/cintel-07-tdash",
        target="_blank",
         )
    ui.a(
        "GitHub Original Project Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
         )
    ui.a(
        "GitHub Orginial App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/Keyoungg2/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


with ui.layout_column_wrap(fill=False):
    #Creating data value box for peguin count  
    with ui.value_box(showcase=icon_svg("earlybirds"), theme="'text-blue"):
        "Number of penguins"#title of value box 

        @render.text
        def count():
            return filtered_df().shape[0]

    #Creating data value box for bill depth
    with ui.value_box(showcase=icon_svg("ruler-horizontal"), theme="text-blue"):
        "Average bill length"#title of value box 

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    #Creating data value box for bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical"), theme="text-blue"):
        "Average bill depth" #title of value box 

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

with ui.navset_card_tab(id="tab"):
    # Creating Scatter plot
    with ui.nav_panel("Plotly scatterplot"):
       ui.card_header("Bill length and depth") #Title for Frame
       @render.plot
       def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )
    with ui.nav_panel("Seaborn Histogram Chart"):
        #Creating interactive data grid
        ui.card(full_screen=True)
        ui.card_header("Penguin data") #Title for Frame #Issue 1 corrected 

        #Details columns c
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
