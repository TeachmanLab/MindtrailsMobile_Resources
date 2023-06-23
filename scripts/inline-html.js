function applyInline(element, filter, filterIn = false, exclude, recursive = true)
{
	element = element || document.body;
	filter = filter || [];
	exclude = exclude || [];

	filter = filter.map(i => i.toLowerCase());
	exclude = exclude.map(i => i.toLowerCase());

	const matches = matchRules(element);

	// we need to preserve any pre-existing inline styles.
	var srcRules = document.createElement(element.tagName).style;

	srcRules.cssText = element.style.cssText;

	matches.forEach(rule =>
	{
		for (var property of rule.style)
		{
			if ((filter.indexOf(property.toLowerCase()) == -1) != filterIn && exclude.indexOf(element.tagName.toLowerCase()) == -1)
			{
				let value = srcRules.getPropertyValue(property) || rule.style.getPropertyValue(property);
				let priority = rule.style.getPropertyPriority(property);

				element.style.setProperty(property, value, priority);
			}
		}
	});

	if (recursive)
	{
		Array.from(element.children).forEach(child =>
		{
			applyInline(child, filter, filterIn, exclude, recursive);
		});
	}

	element.removeAttribute('class');
}

function matchRules(element, sheets)
{
	var matches = [];

	sheets = sheets || document.styleSheets;

	for (var s in sheets)
	{
		if (sheets.hasOwnProperty(s))
		{
			var rules = sheets[s].rules || sheets[s].cssRules;
			for (var r in rules)
			{
				if (element.matches(rules[r].selectorText))
				{
					matches.push(rules[r]);
				}
			}
		}
	}

	return matches;
}
