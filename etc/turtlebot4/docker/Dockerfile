FROM ros:humble

# Add ROS 2 testing server
RUN echo "deb [ signed-by=/usr/share/keyrings/ros2-latest-archive-keyring.gpg ] http://packages.ros.org/ros2-testing/ubuntu jammy main" > /etc/apt/sources.list.d/ros2-testing.list

# install ros packages
RUN apt-get update && apt-get install -y \
      ros-${ROS_DISTRO}-irobot-create-msgs \
      ros-${ROS_DISTRO}-create3-republisher \
      git \
      nano \
      net-tools \
      iputils-ping && \
    rm -rf /var/lib/apt/lists/*

ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user
#RUN groupadd --gid $USER_GID $USERNAME \
#  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
#  # [Optional] Add sudo support for the non-root user
#  && apt-get update \
#  && apt-get install -y sudo \
#  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
#  && chmod 0440 /etc/sudoers.d/$USERNAME \
#  # Cleanup
#  && rm -rf /var/lib/apt/lists/* \
#  && echo "source /usr/share/bash-completion/completions/git" >> /home/$USERNAME/.bashrc \
#  && echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc
