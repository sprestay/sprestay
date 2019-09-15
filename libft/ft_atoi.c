/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 16:29:18 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/07 13:12:53 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static void		znak(char c, int *z)
{
	if (c == '-')
		*z = -1;
	else
		*z = 1;
}

int				ft_atoi(const char *s)
{
	int i;
	int sum;
	int z;
	int	n;

	i = 0;
	sum = 0;
	n = 0;
	while ((s[i] == ' ' || s[i] == '\t' || s[i] == '\n' || s[i] == '\v'
				|| s[i] == '\f' || s[i] == '\r') && s[i] != '\0')
		i++;
	znak(s[i], &z);
	if (s[i] == '-' || s[i] == '+')
		i++;
	while ((*(s + i) >= '0') && (*(s + i) <= '9'))
	{
		sum = sum * 10 + (s[i] - 48);
		i++;
		n++;
		if ((n >= 20) && (z > 0))
			return (-1);
		if ((n >= 20) && (z < 0))
			return (0);
	}
	return (sum * z);
}
