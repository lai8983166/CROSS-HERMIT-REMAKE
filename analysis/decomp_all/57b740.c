
void FUN__text__0057b740(undefined4 *param_1)

{
  int iVar1;
  short *psVar2;
  
  *param_1 = 0;
  psVar2 = (short *)(*DAT_005922c8)(0);
  if ((*psVar2 == 0x5a4d) && (*(int *)(psVar2 + 0x1e) != 0)) {
    iVar1 = *(int *)(psVar2 + 0x1e);
    *(undefined1 *)param_1 = *(undefined1 *)((int)psVar2 + iVar1 + 0x1a);
    *(undefined1 *)((int)param_1 + 1) = *(undefined1 *)((int)psVar2 + iVar1 + 0x1b);
  }
  return;
}

