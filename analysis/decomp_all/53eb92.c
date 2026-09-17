
void FUN__text__0053eb92(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  char *pcVar3;
  bool bVar4;
  char *pcVar5;
  char local_204 [255];
  undefined1 local_105;
  undefined1 local_104 [255];
  undefined1 local_5;
  
  FUN__text__00572640(local_204,0x100,param_2,&stack0x0000000c);
  local_105 = 0;
  if (*(int *)(param_1 + 0x3d8) != 0) {
    iVar1 = 0xd;
    bVar4 = true;
    pcVar5 = local_204;
    pcVar3 = "syntax error";
    do {
      if (iVar1 == 0) break;
      iVar1 = iVar1 + -1;
      bVar4 = *pcVar5 == *pcVar3;
      pcVar5 = pcVar5 + 1;
      pcVar3 = pcVar3 + 1;
    } while (bVar4);
    if (bVar4) {
      iVar1 = *(int *)(param_1 + 0x3dc);
      if (iVar1 == 0) {
        iVar1 = *(int *)(param_1 + 0x1d0);
        pcVar5 = "%s(%d) : (Assembly Error) shader version expected";
      }
      else {
        if (*(int *)(param_1 + 0xa0) != 0) {
          iVar2 = 4;
          bVar4 = true;
          pcVar5 = (char *)(param_1 + 200);
          pcVar3 = "def";
          do {
            if (iVar2 == 0) break;
            iVar2 = iVar2 + -1;
            bVar4 = *pcVar5 == *pcVar3;
            pcVar5 = pcVar5 + 1;
            pcVar3 = pcVar3 + 1;
          } while (bVar4);
          if (bVar4) {
            iVar1 = *(int *)(param_1 + 0x1d0);
            pcVar5 = "%s(%d) : (Assembly Error) constant definition in shader body";
            goto LAB__text__0053ec32;
          }
        }
        pcVar5 = "%s(%d) : (Assembly Error) statement incomplete";
      }
LAB__text__0053ec32:
      FUN__text__005715b0(local_104,0x100,pcVar5,param_1 + 0x1d4,iVar1);
      goto LAB__text__0053ec9d;
    }
  }
  if (*(int *)(param_1 + 0x3e0) == 0) {
    iVar1 = *(int *)(param_1 + 0x1d0);
  }
  else {
    iVar1 = *(int *)(param_1 + 0x3e4);
  }
  if (iVar1 == 0) {
    iVar1 = 1;
  }
  FUN__text__005715b0(local_104,0x100,"%s(%d) : (Assembly Error) %s",param_1 + 0x1d4,iVar1,local_204
                     );
LAB__text__0053ec9d:
  local_5 = 0;
  FUN__text__00548f0a(local_104);
  *(int *)(param_1 + 0xa4) = *(int *)(param_1 + 0xa4) + 1;
  *(undefined4 *)(param_1 + 0x98) = 1;
  return;
}

