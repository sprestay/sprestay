/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strsplit.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 19:48:16 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/07 15:55:03 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int		how_many_words(char const *s, char c)
{
	int		i;
	int		sum;

	i = 0;
	sum = 0;
	if (!s)
		return (0);
	while (s[i] != '\0')
	{
		while (s[i] == c)
			i++;
		if (s[i] != '\0')
			sum++;
		while (s[i] != c && s[i] != '\0')
			i++;
	}
	return (sum);
}

static int		len(char const *s, char c)
{
	int		i;

	i = 0;
	while (s[i] != '\0' && s[i] != c)
		i++;
	return (i);
}

static char		*make_string(char *s1, char const *s, int *k, char c)
{
	int		i;
	int		j;

	i = 0;
	j = *k;
	while (s[j] != c && s[j] != '\0')
	{
		s1[i] = s[j];
		i++;
		j++;
	}
	s1[i] = '\0';
	*k = j;
	return (s1);
}

char			**ft_strsplit(char const *s, char c)
{
	int		i;
	int		j;
	char	**arr;

	i = 0;
	j = 0;
	if (!(arr = (char **)malloc(sizeof(char *) * (how_many_words(s, c) + 1))))
		return (NULL);
	while (j < how_many_words(s, c))
	{
		while (s[i] == c && s[i] != '\0')
			i++;
		arr[j] = (char *)malloc(sizeof(char) * (len(s + i, c) + 1));
		if (arr[j])
			make_string(arr[j], s, &i, c);
		else
		{
			while (j--)
				ft_strdel(&arr[j]);
			return (NULL);
		}
		j++;
	}
	arr[j] = NULL;
	return (arr);
}
