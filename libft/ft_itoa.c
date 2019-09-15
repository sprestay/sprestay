/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/05 08:21:53 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/06 20:42:47 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int		razryad(int n)
{
	int		m;

	m = 1;
	while (n)
	{
		n = n / 10;
		m++;
	}
	if (m > 1)
		m--;
	return (m);
}

static int		znak(int *n, int *f)
{
	int		z;
	int		k;

	z = 0;
	k = *n;
	if (k == -2147483648)
	{
		*f = 1;
		k = k + 1;
	}
	else
		*f = 0;
	if (k < 0)
	{
		z = 1;
		k = -k;
	}
	*n = k;
	return (z);
}

char			*ft_itoa(int n)
{
	char	*num;
	int		z;
	int		m;
	int		f;
	int		a;

	z = znak(&n, &f);
	m = razryad(n);
	if (!(num = (char *)malloc(sizeof(char) * (m + z + 1))))
		return (NULL);
	a = m + z - 1;
	num[m + z] = '\0';
	while (m + z)
	{
		num[m + z - 1] = n % 10 + 48;
		n = n / 10;
		m--;
	}
	if (f)
		num[a] = num[a] + 1;
	if (z)
		num[0] = '-';
	return (num);
}
