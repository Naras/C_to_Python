#include <stdio.h>
#include <conio.h>
#include <string.h>
#include <stdlib.h>
#include "data.h"
#include "header.h"

int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean)
{
	int yes=0,success=1;

	while(1)
	{
		if((tvibptr->stype =='1' && strcmp(tvibptr->specf,"dative")==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4')
		{
		/* Check for case where there is only a single meaning for ������� ��˳��� */
			yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);

			if(tvibptr->stype=='2' && tvibptr->matnoun !=1 )
			{
				switch(tvibptr->spos)
				{
					case 0:
						if(tvibptr->semlinga==0)
							strcat(tvibptr->arthaword,"�� ");
						if(tvibptr->semlinga==1)
							strcat(tvibptr->arthaword,"ף ");
						if(tvibptr->semlinga==2)
							strcat(tvibptr->arthaword,"��� ");
						break;
					case 1:
						strcat(tvibptr->arthaword,"������辳���������ȳ ");
						break;
					case 2:
						strcat(tvibptr->arthaword,"���辳��������ȳ ");
						break;
					case 3:
						strcat(tvibptr->arthaword,"�������������������ȳ ");
						break;
					case 4:
						strcat(tvibptr->arthaword,"����������������ȳ ");
						break;
					case 5:
						strcat(tvibptr->arthaword,"������۳��������ȳ ");
						break;
				}
			}
			if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5')
				success= 0;

		}
		if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,"object")==0))
		{
		       /* Check for case where there is only a single meaning for �������� ��˳��� */
			yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);
		}


/* If not in above case following steps lead to menu display for
   selection based on type of vibhakti */
		 if(tvibptr->stype =='1')
		 {
			 switch(tvibptr->spos)
			 {
				case 0:
					if(strcmpi(voice,"kartari") ==0)
						strcpy(tvibptr->arthaword,tvibptr->sword);
					if(strcmpi(voice,"karmani") ==0)
					{
						strcpy(tvibptr->arthaword,tvibptr->bword);
						strcat(tvibptr->arthaword,"���辳����������ȳ ");
					}
					break;

				case 1:
					if(strcmpi(voice,"kartari") ==0)
					{
						strcpy(tvibptr->arthaword,tvibptr->bword);
						strcat(tvibptr->arthaword,"���辳���������ȳ ");
					}
					if(strcmpi(voice,"karmani") ==0)
					{
						strcpy(tvibptr->arthaword,tvibptr->sword);
					}
					break;
				 case 2:
					strcpy(tvibptr->arthaword,tvibptr->bword);
					strcat(tvibptr->arthaword,"���辳��������ȳ ");
					break;
				 case 3:
					strcpy(tvibptr->arthaword,tvibptr->bword);
					strcat(tvibptr->arthaword,"�������������������ȳ ");
					break;
				 case 4:
					strcpy(tvibptr->arthaword,tvibptr->bword);
					strcat(tvibptr->arthaword,"����������������ȳ ");
					break;
				 case 6:
					strcpy(tvibptr->arthaword,tvibptr->bword);
					strcat(tvibptr->arthaword,"�������� ");
					break;
				 case 5:
					strcpy(tvibptr->arthaword,tvibptr->bword);
					strcat(tvibptr->arthaword,"������۳��������ȳ ");
					break;
			}
		 }
		 if (tvibptr->next != NULL)
			tvibptr=tvibptr->next;
		 else
		 	break;
	}
	return success;
}


