/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 18:14:25 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/08 10:23:21 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnew(size_t size)
{
	char *res;

	res = (char *)malloc(sizeof(char) * size + 1);
	if (res)
	{
		res[size] = '\0';
		while (size--)
			res[size] = '\0';
		return (res);
	}
	else
		return (NULL);
}
