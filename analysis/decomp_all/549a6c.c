
void FUN__text__00549a6c(int param_1)

{
  undefined4 *puVar1;
  
  puVar1 = (undefined4 *)(*(code *)**(undefined4 **)(param_1 + 4))(param_1,0,0x18);
  *(undefined4 **)(param_1 + 0x18c) = puVar1;
  *(undefined1 *)(puVar1 + 4) = 0;
  *(undefined1 *)((int)puVar1 + 0x11) = 0;
  *puVar1 = &LAB__text__00549991;
  puVar1[1] = FUN__text__00549a24;
  puVar1[2] = FUN__text__00549957;
  puVar1[3] = &LAB__text__00549a5b;
  *(undefined1 *)(puVar1 + 5) = 1;
  return;
}

