/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 14:51:09 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/05 18:21:36 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strstr(const char *hays, const char *need)
{
	int		i;
	int		j;

	i = 0;
	if (need[0] == '\0')
		return ((char *)hays);
	while (hays[i] != '\0')
	{
		j = 0;
		while (hays[i + j] == need[j] && need[j] != '\0' &&
				hays[i + j] != '\0')
			j++;
		if (need[j] == '\0')
			return ((char *)hays + i);
		i++;
	}
	return (NULL);
}
