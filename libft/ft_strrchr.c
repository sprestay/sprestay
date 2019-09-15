/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 14:47:37 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/06 09:17:15 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *str, int ch)
{
	int		i;

	i = 0;
	while (str[i] != '\0')
		i++;
	if (str[i] == (unsigned char)ch)
		return ((char *)str + i);
	i--;
	while (i >= 0)
	{
		if (str[i] == (unsigned char)ch)
			return ((char *)str + i);
		i--;
	}
	return (NULL);
}
