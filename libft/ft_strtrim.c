/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 19:29:44 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/07 15:21:57 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strtrim(char const *s)
{
	int		st;
	int		fin;

	st = 0;
	if (!s)
		return (NULL);
	fin = ft_strlen(s) - 1;
	while ((s[fin] == ' ' || s[fin] == '\t' || s[fin] == '\n') && fin > 0)
		fin--;
	while ((s[st] == ' ' || s[st] == '\t' || s[st] == '\n') && st < fin)
		st++;
	if (st == fin)
		return (ft_strnew(1));
	return (ft_strsub(s, st, fin - st + 1));
}
