/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 14:40:30 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/06 09:13:53 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strchr(const char *str, int ch)
{
	size_t		i;

	i = 0;
	while (str[i] != (unsigned char)ch && str[i] != '\0')
		i++;
	if (str[i] == '\0' && str[i] != (unsigned char)ch)
		return (NULL);
	else
		return ((char *)str + i);
}
