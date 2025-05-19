# HomeAssistantTibber
fork of the home assistant tibber component with some extra features:

- You can set a tax rate, surchage fee and tax per kWh
- Components calculated different energy prices per kWh prices based on settings above
- four sensors indicate the current hour's ranking today, so you can make autmations based on whether the current hour is within the cheapest X hours

Automation based on ranking for cheapest 4 hours in the night

![Screenshot 2024-06-01 at 14-07-20 Instellingen – Home Assistant](https://github.com/brupje/HomeAssistantTibber/assets/2556592/67eebb76-9e70-447b-bedd-5935c6003587)


Overview of available sensors (base price shown here is €0.00)
![Screenshot 2024-06-01 at 14-11-57 Overzicht – Home Assistant](https://github.com/brupje/HomeAssistantTibber/assets/2556592/7450e953-2285-4f48-bbff-2f6fbf74a1b6)


Useful for people with excess solar power energy in The Netherlands, where you get tax back for produced solar power.

Taxes are here : https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/overige_belastingen/belastingen_op_milieugrondslag/energiebelasting/
and the cost Tibber are here , you need to extract the tax from it. example 0,1228 incl 21% the it will be 0.097012 Surcharge price per KWH Excl Tax*
https://support.tibber.com/nl/articles/5605892-de-kosten-bij-tibber

