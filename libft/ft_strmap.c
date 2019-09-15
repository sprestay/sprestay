/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 18:39:04 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/07 13:18:03 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strmap(char const *s, char (*f)(char))
{
	char	*fr;
	int		i;

	if (!s || !f)
		return (NULL);
	i = 0;
	if (!(fr = (char *)malloc(sizeof(char) * (ft_strlen(s) + 1))))
		return (NULL);
	while (s[i] != '\0')
	{
		fr[i] = f(s[i]);
		i++;
	}
	fr[i] = '\0';
	return (fr);
}
